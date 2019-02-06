# Controllerについて

####  構造
-  index側にSQLを用いてグラフに用いるデータの取得を行っている。

##### SQLで問い合わせた内容
1. 計測している温度と推定温度のテーブルを結合して取得
2. 温度と同じく湿度も推定湿度のテーブルと結合して取得
3. UIに表示するための値を取得

#### プログラム
 ~~~
 <?php
 App::uses('AppController', 'Controller');
 /**
  * Environments Controller
  *
  * @property Environment $Environment
  * @property PaginatorComponent $Paginator
  * @property SessionComponent $Session
  * @property FlashComponent $Flash
  */
 class EnvironmentsController extends AppController {

 /**
  * Components
  *
  * @var array
  */
     public $components = array('Paginator', 'Session', 'Flash');
     //レイアウトの読み込み
     public $layout = 'origiLay';
 /**
  * index method
  *
  * @return void
  */
     public function index() {
         $this->Environment->recursive = 0;
         $this->set('environments', $this->Paginator->paginate());
         $this->set('openweathers', $this->Paginator->paginate());
~~~

##### ・温度の取り出し     
~~~

    //arpredicts : environments の結合 (15分毎に揃えて温度を取り出し）
    $PEsql  = "SELECT P.pdate, P.predtemp,  E.temperature FROM (SELECT from_unixtime(round(unix_timestamp(pdatetime) div (15 * 60)) * (15 * 60)) AS pdate,predtemp FROM arpredicts GROUP BY pdate DESC LIMIT 96) AS P LEFT OUTER JOIN (SELECT from_unixtime(round(unix_timestamp(uploaded) div (15 * 60)) * (15 * 60)) AS upload,temperature FROM environments GROUP BY upload DESC LIMIT 96) AS E  ON P.pdate = E.upload;";
    $PEdatas = $this->Environment->query($PEsql, false);
    $this->set('PEtemps', $PEdatas);

~~~
センサーからの値が入っているテーブルと推定温度が入っているテーブルの温度のみを15分間隔にデータをまとめた上で,
　テーブルの結合をして取り出し、index側に受け渡す。

~~~

     //arpredicts : environments の結合(15分毎に揃えて気温を取り出し）
     $PEsql2 = "SELECT P.pdate, P.predhumid,  E.humid FROM (SELECT from_unixtime(round(unix_timestamp(pdatetime) div (15 * 60)) * (15 * 60)) AS pdate,predhumid FROM arpredicts GROUP BY pdate DESC LIMIT 96) AS P LEFT OUTER JOIN (SELECT from_unixtime(round(unix_timestamp(uploaded) div (15 * 60)) * (15 * 60)) AS upload,humid FROM environments GROUP BY upload DESC LIMIT 96) AS E  ON P.pdate = E.upload;";
     $PEdatas2 = $this->Environment->query($PEsql2, false);
     $this->set('PEhumids', $PEdatas2);
~~~
気温側と同じく15分毎にデータをまとめた上でテーブルを結合して取り出し、index側に受け渡す。

~~~
         //OpenWhethers(外気温の取り出し)
         $Osql = "select * from openweathers order by id desc LIMIT 96;";
         $Odatas = $this->Environment->query($Osql, false);
         $this->set('openweathers', $Odatas);
~~~
外気のデータを格納しているテーブルからデータを取り出しindexに受け渡す。

~~~
         //prediction(UIに表示するために予測温度の最新の値を取り出し)
         $this->set('arpredicts', $this->Paginator->paginate());
         $pSql = "select predtemp from arpredicts where id =(select max(id) from arpredicts);";
         $Pdata = $this->Environment->query($pSql, false);
         $Pdata2 = $Pdata[0]['arpredicts']['predtemp'];
         $this->set('arpretemp', $Pdata2);

         //roomTemp(UIに表示するために温度の最新の値を取り出し)
         $Rsql = "select temperature from environments where id = (select max(id) from environments);";
         $Rdata = $this->Environment->query($Rsql, false);
         $Rdata2 = $Rdata[0]['environments']['temperature'];
         $this->set('roomTemp', $Rdata2);
         
         //comfortV
         $this->set('arpredicts', $this->Paginator->paginate());
         $pSql2 = "select predcomfort from arpredicts where id =(select max(id) from arpredicts);";
         $Pdata3 = $this->Environment->query($pSql2, false);
         $Pdata4 = $Pdata3[0]['arpredicts']['predcomfort'];
         $this->set('arcom', $Pdata4);

     }
 }

 ?>
~~~
UIに表示するためにmax()を用いてテーブル内の最新データのみを取り出して、indexに受け渡す。
取り出すものは現在気温・推定気温・不快指数の３種
#### 備考
-  SQLを実行する際にOptionに'false'をつけることでクエリ実行をキャッシュしないようにすることで、メモリの消費を抑える
-  15分毎1日分のみを取り出す為に取り出し件数を96件としている
