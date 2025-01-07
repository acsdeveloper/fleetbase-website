<?php
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

require_once 'vendor/autoload.php';

$dotenv = Dotenv\Dotenv::createImmutable(__DIR__);
$dotenv->safeLoad();

// Check if the request method is POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Only POST requests are allowed']);
    exit;
}

// Check if the content type is JSON
if ($_SERVER['CONTENT_TYPE'] !== 'application/json') {
    http_response_code(415);
    echo json_encode(['error' => 'Content type must be application/json']);
    exit;
}

// Get the JSON input
$input = json_decode(file_get_contents('php://input'), true);

// Check if the token is present and valid
$validToken = $_ENV['SECRET_TOKEN'] || 'secret-token';
$headers = getallheaders();
if (!isset($headers['token']) || $headers['token'] !== $validToken) {
    http_response_code(401);
    echo json_encode(['error' => 'Invalid or missing token']);
    exit;
}

$mail = new PHPMailer(true);

try {
    //Server settings
    $mail->SMTPDebug = 2;                                       // Enable verbose debug output
    $mail->isSMTP();                                            // Set mailer to use SMTP
    $mail->Host       = $_ENV['SMTP_HOST'];                    // Specify main and backup SMTP servers
    $mail->SMTPAuth   = true;                                   // Enable SMTP authentication
    $mail->Username   = $_ENV['SMTP_USERNAME'];                // SMTP username
    $mail->Password   = $_ENV['SMTP_PASSWORD'];                // SMTP password
    $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;         // Enable TLS encryption, `ssl` also accepted
    $mail->Port       = $_ENV['SMTP_PORT'];                    // TCP port to connect to

    //Recipients
    $mail->setFrom($_ENV['MAIL_FROM_ADDRESS']);
    $mail->addAddress('developer@agilecyber.com');           // Add a recipient
    // $mail->addReplyTo('info@example.com', 'Information');

    // Content
    $mail->isHTML(true);                                        // Set email format to HTML
    $mail->Subject = 'New Contact Form Submission';
    $mail->Body    = 'You have received a new message from your website contact form.<br><br>' .
                     '<b>First Name:</b> ' . htmlspecialchars($input['first-name']) . '<br>' .
                     '<b>Last Name:</b> ' . htmlspecialchars($input['last-name']) . '<br>' .
                     '<b>Email:</b> ' . htmlspecialchars($input['email']) . '<br>' .
                     '<b>Message:</b> ' . nl2br(htmlspecialchars($input['message'])) . '<br>';
    $mail->AltBody = 'You have received a new message from your website contact form.' . "\n\n" .
                     'First Name: ' . htmlspecialchars($input['first-name']) . "\n" .
                     'Last Name: ' . htmlspecialchars($input['last-name']) . "\n" .
                     'Email: ' . htmlspecialchars($input['email']) . "\n" .
                     'Message: ' . htmlspecialchars($input['message']);

    $mail->send();

    http_response_code(200);
    echo json_encode(['success' => true, 'message' => 'Message has been sent']);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'error' => "Message could not be sent. Mailer Error: {$mail->ErrorInfo}"]);
}