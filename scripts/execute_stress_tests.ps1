Set-PSDebug -Trace 1
Get-ChildItem samples | ForEach-Object {
  $InputPath = ".\samples\$_"
  python .\ontodl.py $InputPath -f log | Out-Null
  python .\ontodl.py $InputPath -f json | Out-Null
  python .\ontodl.py $InputPath -f dot:experimental | Out-Null
  python .\ontodl.py $InputPath -f dot | Out-Null
  python .\ontodl.py $InputPath -f prolog | Out-Null
  python .\ontodl.py $InputPath -f owl | Out-Null
}
Set-PSDebug -Trace 0