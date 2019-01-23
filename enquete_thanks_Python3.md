##### Python3のパスは機種依存のため $ which pythonで調べること
```
$path = '/usr/bin/python3';
```
##### Pythonファイルを実行
```
$cmd = $path." ./transDb.py"." ".$place." ".$comfort." ".$airflg." ".$airtemp." ".$airmode;
$fullPath = $cmd;

exec($fullPath, $outpara, $returnpara);
```