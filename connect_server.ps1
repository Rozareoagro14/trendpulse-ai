# PowerShell скрипт для подключения к серверу
$password = "W5AV!54uq@5EMXLA"
$server = "root@45.142.122.145"

# Создаем процесс SSH
$process = Start-Process -FilePath "ssh" -ArgumentList $server -NoNewWindow -PassThru -RedirectStandardInput -RedirectStandardOutput -RedirectStandardError

# Отправляем пароль
$process.StandardInput.WriteLine($password)

# Ждем завершения
$process.WaitForExit() 