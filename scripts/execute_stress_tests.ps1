Get-ChildItem samples | ForEach-Object {
  $InputPath = ".\samples\$_"
  Write-Output "Processing $InputPath"
  python .\ontodl.py $InputPath -f log | Out-Null
  python .\ontodl.py $InputPath -f json | Out-Null
  python .\ontodl.py $InputPath -f dot | Out-Null
}