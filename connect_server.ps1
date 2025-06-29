# PowerShell скрипт для подключения к серверу
$password = "[ВАШ_ПАРОЛЬ_СЕРВЕРА]"

# Создание процесса SSH
$process = Start-Process -FilePath "ssh" -ArgumentList "root@trashy-leg" -NoNewWindow -PassThru -RedirectStandardInput

# Отправка пароля
$process.StandardInput.WriteLine($password)

# Ожидание завершения
$process.WaitForExit() 