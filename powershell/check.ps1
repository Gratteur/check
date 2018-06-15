Write-Host "spooky"

$oldHashrate = 0

while($true){
    $res=$null
	Write-Host ""
	$a = Get-Date
	$a.ToUniversalTime()
	$res = Invoke-WebRequest -UseBasicParsing -Uri http://127.0.0.1:203/api.json -TimeoutSec 20
	Write-Host "response_size = $($res.length)"
	$data = $res | ConvertFrom-Json
	$newHashrate = $data.hashrate.total[0]

	If ($res.length -ne 1)
	{
                Write-Host "restarting1"
                cmd.exe /c 'shutdown -r -f -t 5'
	}

	If ($newHashrate -ge 3800 -OR $newHashrate -eq $null)
	{
		Write-Host "oldHashrate = $($oldHashrate)"
		Write-Host "newHashrate = $($newHashrate)"
		$oldHashrate = $newHashrate
	}

	Else
	{
		Write-Host "restarting"
		cmd.exe /c 'shutdown -r -f -t 5'
	}

	sleep 30
}

Write-Host "boi"
