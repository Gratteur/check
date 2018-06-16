	$a = Get-Date
	$a.ToUniversalTime()
	$res = Invoke-WebRequest -UseBasicParsing -Uri http://ripmundocrit.ddns.net:1000/api -TimeoutSec 20
	$data = $res | ConvertFrom-Json
	$switch = $data.result.switch
    $coin = $data.result.coin_to_mine

    If ($switch -eq 0)
	{
                Write-Host "Alles klar"
	}

	ElseIf ($coin -eq 1)
	{
		Write-Host "Changing to Electroneum"
        C:\Mining\Coin\Electroneum.bat
        Write-Host "Rebooting in 30sec"
        cmd.exe /c 'shutdown -r -f -t 30'
	}

	ElseIf ($coin -eq 2)
	{
		Write-Host "Changing to Graft"
        C:\Mining\coin\Graft.bat
        Write-Host "Rebooting in 30sec"
		cmd.exe /c 'shutdown -r -f -t 30'
	}
