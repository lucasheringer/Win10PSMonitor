﻿while ($true) {
Clear-Host
#reading CPU load percentage
#$percent = Get-WmiObject win32_processor | select LoadPercentage 
#Write-Host $percent[0]
#$key, $value = $percent[0] -split '='
#Write-Host $value.Substring(0,$value.Length-1)

#Another way to get cpu load
$avg = Get-WmiObject win32_processor | Measure-Object -property LoadPercentage -Average | Foreach {$_.Average}
Write-Host $avg

#reading memory usage
$mem = Get-WmiObject win32_operatingsystem | Foreach {"{0:N2}" -f ((($_.TotalVisibleMemorySize - $_.FreePhysicalMemory)*100)/ $_.TotalVisibleMemorySize)}
Write-Host $mem

#Getting IO disk percentage

$numRep=3
$Sleep=2
$Idle1=$DiskTime1=$T1=$Idle2=$DiskTime2=$T2=$numRep=3

$Disk = Get-WmiObject -class Win32_PerfRawData_PerfDisk_LogicalDisk `
-filter "name= '_Total' "
[Double]$Idle1 = $Disk.PercentIdleTime
[Double]$DiskTime1 = $Disk.PercentDiskTime
[Double]$T1 = $Disk.TimeStamp_Sys100NS

start-Sleep $Sleep

$Disk = Get-WmiObject -class Win32_PerfRawData_PerfDisk_LogicalDisk `
-filter "name= '_Total' "
[Double]$Idle2 = $Disk.PercentIdleTime
[Double]$DiskTime2 = $Disk.PercentDiskTime
[Double]$T2 = $Disk.TimeStamp_Sys100NS

#$PercentIdleTime =(1 - (($Idle2 - $Idle1) / ($T2 - $T1))) * 100
#"`t Percent Disk Idle Time is " + "{0:n2}" -f $PercentIdleTime
$PercentDiskTime =(1 - (($DiskTime2 - $DiskTime1) / ($T2 - $T1))) * 100
"{0:n2}" -f $PercentDiskTime

#writing to file
$Logfile = "D:\Monitor.log"

$all = $avg.ToString() + ", " + $mem.ToString() + ", " + "{0:n2}" -f $PercentDiskTime
Write-Host $all
#Add-content -Path $Logfile -Value $avg $mem 

#Sleeping
start-sleep -s 2
}