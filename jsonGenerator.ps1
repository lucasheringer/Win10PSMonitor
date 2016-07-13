#PowerShell to read the CSV with data and load into a json

$myFileName = "C:\Users\lucas\Downloads\OpenHardwareMonitor\OpenHardwareMonitorLog-2016-07-08.csv"

#Example of how to get the last 3 rows
#$LastThreeRowsArray = (Get-Content $myFileName)[-1 .. -3]

# Get last one row of file into variable
$lastDataRow = (Get-Content $myFileName)[-1]

#parse the CSV data back into separate variables, one for each column
$dataArray = $lastDataRow.Split(",")
$lastRowDate = [DateTime] $dataArray[0]  #convert back to DateTime datatype
$lastRowStatus = $dataArray[5]
$lastRowAction = $dataArray[10]
$lastRowKeyword = $dataArray[19]

Write-Host "`$lastDataRow=$lastDataRow"
Write-Host "Date=$lastRowDate"
Write-Host "CPULoad=$lastRowStatus"
Write-Host "CPUTemp=$lastRowAction"
Write-Host "MEMUsage=$lastRowKeyword"

#$currentDateTime = get-date

#$dateTimeDiff = $currentDateTime  - $lastRowDate
#$minutesDiff = $dateTimeDiff.Minutes
#$totalMinutesDiff = $dateTimeDiff.TotalMinutes
#Write-Host "`$currentDateTime =$currentDateTime"
#Write-Host "`$dateTimeDiff=$dateTimeDiff"
#Write-Host "`$minutesDiff=$minutesDiff "
#Write-Host "`$totalMinutesDiff=$totalMinutesDiff "
