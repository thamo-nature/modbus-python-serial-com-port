<?php

//add db and phpmailer files links

include_once("../includes/database.php");

$data = json_encode($_POST);
$para_meter = json_decode($data);
$total_chart_vessels_count =  $para_meter->total_vessel_count;
$total_connected_charts = $para_meter->total_connected_charts;

$array = json_decode($para_meter->charts, true);

$not_connected_array = json_decode($para_meter->not_connected_charts, true);

print_r($not_connected_array);
print_r($array);

print_r(Count($array));

function send_alert_mail(array $final_arr_faulty_vessels , $total_chart_vessels_count , $total_connected_charts , $alert_users_no_response)
{

    global $database;

    require('PHPMailer/class.phpmailer.php');
    require('PHPMailer/class.smtp.php');

    $final_arr = $final_arr_faulty_vessels;

    print_r($final_arr);
    
    $get_alert_array = array();

    $alert_array = array();

    foreach ($final_arr as $par_chart_vessel) {

        $tempa = $par_chart_vessel['tempa'];
        $tempb = $par_chart_vessel['tempb'];
        $level = $par_chart_vessel['level'];
        $chart_vessel_number = $par_chart_vessel['vessel'];

        
        if (($tempa >= -190) or ($tempb >= -160) or ($level >10 or $level < 8)) {

            $get_alert_array[] = array('vessel_no' => $chart_vessel_number, 'tempa' => $tempa, 'tempb' => $tempb, 'level' => $level);
        }
    }

     print_r($get_alert_array);

     print_r(count($get_alert_array));

    

    foreach ($get_alert_array as $inspect_alert_to_send) {
        if ($inspect_alert_to_send['tempa'] >= -190) {
            $a_tempa = "<span style='color:red'>" . $inspect_alert_to_send['tempa'] . "</span>";
        } else {
            $a_tempa = $inspect_alert_to_send['tempa'];
        }

        if ($inspect_alert_to_send['tempb'] >= -160) {
            $a_tempb = "<span style='color:red'>" . $inspect_alert_to_send['tempb'] . "</span>";
        } else {
            $a_tempb = $inspect_alert_to_send['tempb'];
        }

        if (($inspect_alert_to_send['level'] > 10 or $inspect_alert_to_send['level'] < 8)) {
            $a_level = "<span style='color:red'>" . $inspect_alert_to_send['level'] . "</span>";
        } else {
            $a_level =  $inspect_alert_to_send['level'];
        }

        $alert_array[] = array($inspect_alert_to_send['vessel_no'], $a_tempa, $a_tempb, $a_level);
    }

    print_r($alert_array);
    $vessels_with_alert_issues = (count($alert_array));
    $total_number_of_not_connected_charts = $total_chart_vessels_count - $total_connected_charts;

    $e_sql = "select * from alert_email where role='cryo'";
    $result = $database->connection->query($e_sql);
    $date = date("Y-m-d h:i:s");
    $h_read_time = date("F jS, Y", strtotime("now")) . " " . date("h:i:s");

    $message_body = "
    Check the following  Vessels during $h_read_time <br>
    
    Total number of Vessels : $total_chart_vessels_count <br>

    Number of vessels connected : $total_connected_charts <br>

    Number of vessels which has issues :  $vessels_with_alert_issues as follows

    <table style='border-collapse:collapse;margin:25px 0;font-size:0.9em;font-family:sans-serif;box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);'>
    <thead style='background-color: #009879;color: #ffffff;text-align: left;'>
        <tr style='background-color: #009879;color: #ffffff;text-align: left;'>
            <th>Vessel</th>
            <th>TEMPA</th>
            <th>TEMPB</th>
            <th>Level</th>

        </tr>
    </thead>
    <tbody>";

    foreach ($alert_array as $alert_parameters) {

        //var_dump($alert_parameters);
        $chart_vessel_id_alert = $alert_parameters[0];
        $chart_vessel_tempa_alert = $alert_parameters[1];
        $chart_vessel_tempb_alert = $alert_parameters[2];
        $chart_vessel_level_alert = $alert_parameters[3];

        $message_body .= "
         <tr style='padding:12px 15px;'>
             <td> $chart_vessel_id_alert </td>
             <td> $chart_vessel_tempa_alert </td>
             <td> $chart_vessel_tempb_alert </td>
             <td> $chart_vessel_level_alert</td>
          </tr><br>";
    }

    if($total_number_of_not_connected_charts > 0)
    {
        $message_body .= " 
        <h5 style='color:yellow'>Warning unable to connect following vessels</h5>
        Total Chart-Vessels Not Connected : $total_number_of_not_connected_charts
        ";
    }

    foreach ($alert_users_no_response as $no_response_from_server_alert_the_user) {

        $warning_data_vessels = "<h5 style='color:yellow'>$no_response_from_server_alert_the_user</h5>";

        $message_body .= "
            
            $warning_data_vessels ";
    }

    $message_body .= "
    Alert Generated at time $date
    </tbody>
    </table>";

    $mail = new PHPMailer();
    $mail->IsSMTP();
    $mail->SMTPDebug = 1;
    $mail->SMTPAuth = true;
    $mail->SMTPSecure = 'ssl'; // tls or ssl
    $mail->Port = "465";
    $mail->Username = "thamothiran.s@spovum.com";
    $mail->Password = "exvpdktfvnxswbxt";
    $mail->Host = "smtp.gmail.com";
    $mail->Mailer = "smtp";
    $mail->SetFrom("thamothiran.s@spovum.com", "From SpOvum");

    while ($row = mysqli_fetch_array($result)) {
        $users = $row['email'];
        $email = $users;
        $mail->AddAddress($email);
    }

    $mail->Subject = "Alert For Gold Sim Vessels";
    $mail->MsgHTML($message_body);
    $mail->IsHTML(true);
    $result = $mail->Send();

    return $result;

}

//insert to db
foreach ($array as $item) { //foreach element in $arr

  $vessel = $item["vessel"];

  $temp_a = $item["tempa"];
  $tempa = round($temp_a, 1);

  $temp_b = $item["tempb"];
  $tempb = round($temp_b, 1);

  $leve = $item["level"];
  $level = round($leve, 1);

  $usage = $item["usage"];


  if (!empty($para_meter->charts)) {
    $sql = "INSERT INTO cannister_data VALUES (NULL,'$vessel', '$tempa', '$tempb','$level','$usage',NULL)";

    if ($database->connection->query($sql) === TRUE) {
      echo "New record created successfully";
    } else {
      echo "Error: " . $sql . "<br>" . $database->connection->error;
    }
  }
}

//call mail alert
//send_alert_mail($array, $total_chart_vessels_count , $total_connected_charts , $not_connected_array);
