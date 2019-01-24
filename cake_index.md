# Web確認画面について

- 構造
 - ハンバーガーメニュー
 - グラフ表示(室内気温、室内湿度、外気温度・湿度)
 - 現在の温度＋１５分後の推定温度表示


#### 1.ハンバーガーメニュー

-   普段は画面の左端に縮められている。
-   画面左上にあるボタンを押すと右にスライドして画面が出てくる。
-   その画面にあるボタンを押すことで室内グラフと室外グラフを切り替えられる。
-   ボタンの種類は[室内・室外・ON・OFF]の４種である。
~~~
<!-- 普段は非表示状態に成っている　アイコンが押されたらメニューをcssにしたがって表示する -->

<div id = "nav-drawer">
  <input id = "nav-input" type = "checkbox" class = "nav-unshown">
  <label id = "nav-open" for = "nav-input">
    <span></span>
    <span></span>
    <span></span>
  </label>
  <label class = "nav-unshown" id = "nav-close" for = "nav-input">
  </label>

<!-- メニューコンテンツ -->
  <div id = "nav-content" >
    <div class = "nav-table">

      <!-- グラフ等の　表示 / 非表示　切り替え　ボタン -->

      <table  cellpadding="0" cellspacing="0">
         <tr>
           <th><p>グラフの切り替え</p></th>
         </tr>

         <div class ="b">
           <tr>
             <th>グラフの表示/非表示</th>
           </tr>
           <tr>
             <td>
               <input type = "button" class= "btnOn" value = "ON">
               <input type = "button" class= "btnOff" value = "OFF">
             </td>
           </tr>
           <tr>     
             <th>室内/屋外</th>
           </tr>
           <tr>
             <td>
               <input type = "button" class = "btnR" value = "室内">
               <input type = "button" class = "btnO" value = "屋外">
             </td>
           </tr>
         </div>
      </table>
    </div>
  </div>
</div>
~~~

#### 2.グラフ表示
- 温度・湿度・外気の順に縦にグラフを表示する。
- 温度・湿度のグラフには現在の値と計算で出された推定の値の２線を表示する。
- 推定値の線は点線で表示している。またグラフの下限・上限は取得したデータの値に合わせて変わる
- ##### 室内温度表示グラフのプログラム

~~~
<html>
  <head>
    <!--Load the AJAX API-->
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
  </head>
</html>

<div　style = "margin: 0% 10% 0% 5%">
  <script type="text/javascript">
    google.charts.load('current', {packages: ['corechart', 'line']});
    google.charts.setOnLoadCallback(drawBasic);
    function drawBasic() {
      var data = new google.visualization.DataTable(
      );
      data.addColumn('datetime', 'date');
      data.addColumn('number', '気温');
      data.addColumn('number', '予測気温');
      <?php $max = 0;
            $min = 99;
      ?>
      data.addRows([
         <?php foreach($PEtemps as $PEtemp):
           //グラフへの値入力処理
           $temp = $PEtemp['E']['temperature'];
           $predtemp = $PEtemp['P']['predtemp'];
           $upload = $PEtemp['P']['pdate'];

           ##グラフの下限・上限を設定する処理
           if($max < $temp or $max < $predtemp ){
             if($temp < $predtemp){
               $max = $predtemp;
             }else{
               $max = $temp;
             }
           }

           if($min > $temp or $min > $predtemp){
             if($predtemp < $temp){
               $min =  $predtemp;
             }else if(!is_null($temp)){
               $min = $temp;
             }
           }

           //グラフへの入力処理
           echo "[" ?> new Date(
           <?php echo substr($upload,0, -15)?>,
           <?php echo substr($upload, 5, -12)-1?>,
           <?php echo substr($upload, 8, -9)?>,
           <?php echo substr($upload, 11, -6)?>,
           <?php echo substr($upload, 14, -3)?>,
           <?php echo substr($upload, 17)?>)
           <?php echo ",".$temp.",".$predtemp."],"?>
        <?php endforeach?>
      ]);

      //グラフのオプション設定
      var options = {
        hAxis: {
          title: '時間(24時間)'
        },
        vAxis: {
          title: '温度(temp)',
          minValue: <?php echo $min?>,
          maxValue: <?php echo $max+1 ?>
        },
        series:{
          1: { lineDashStyle: [4, 4] },
        },
        colors:['#4169e1', '#ff4500']
      };

      var chart = new google.visualization.LineChart(document.getElementById('chart_divTe'));
      chart.draw(data, options);
    }
  </script>

  <body>
    <div id="chart_divTe" style="width: 900px; height: 500px"></div>
  </body>
</div>
~~~


- 湿度・外気のグラフも同様のプログラムで表示している。
- 変更点は主に繰り返し文の変数への代入部分である。
    ~~~
    ## 変更点(室内湿度)
        foreach($PEhumids as $PEhumid):

           $humid = $PEhumid['E']['humid']; 　
           $predhumid = $PEhumid['P']['predhumid'];
           $upload = $PEhumid['P']['pdate'];

    ## 変更点(外気)

    <div style = "margin: 0% 10% 0% 5%">
        foreach($openweathers as $openweather):

          //グラフへの値入力処理
          $temp = $openweather['openweathers']['temp'];
          $humid = $openweather['openweathers']['humid'] * 100;
          $upload =  $openweather['openweathers']['uploaded'];
    ~~~

#### 3. 現在の温度と推定温度の表示
- 現在の温度と15分後の推定温度を表示している。
- モニターのような背景の中に数字を出すようなデザインである。

    ~~~
        <div class = 'ui'　style="margin: 5% 10% 10% 5%">
          <canvas id = "canvas_O" width = "500" height="500"></canvas>
            <script type="text/javascript">
            monitorUI();
            </script>
         </div>
    ~~~

    - ##### monitorUI()の宣言部分、　monitorUI内で呼び出している関数

    ~~~
        <script type = "text/javascript">

          function getTemp(){
              var returnTemp = '0';
              returnTemp =<?php  echo '"'.$roomTemp.'"' ?>;
              return returnTemp;
          }

          function getCTemp(){
              var returnTemp = '0';
              returnTemp = <?php echo '"'.$arpretemp.'"'?>;
              return returnTemp;
          }

          function monitorUI(){
            //*********************初期設定***********************
              //四角　後ろ
               var rect_canvasB = document.getElementById("canvas_O");
               var rect_ctxB = rect_canvasB.getContext("2d");
               rect_ctxB.beginPath();
               //四角　前
               var rect_canvasF = document.getElementById("canvas_O");
               var rect_ctxF = rect_canvasF.getContext("2d");
               rect_ctxF.beginPath();
               //枠 横上
               var rect_frameA = document.getElementById("canvas_O");
               var rect_frameA_ctx = rect_frameA.getContext("2d");
               rect_frameA_ctx.beginPath();
               //枠 横下
               var rect_frameU = document.getElementById("canvas_O");
               var rect_frameU_ctx = rect_frameU.getContext("2d");
               rect_frameU_ctx.beginPath();
               //枠　縦
               var rect_frameV = document.getElementById("canvas_O");
               var rect_frameV_ctx = rect_frameV.getContext("2d");
               rect_frameV_ctx.beginPath();
               //室温　タイトル
               var draw_rtmpt = document.getElementById("canvas_O");
               var rtmpt_ctx = draw_rtmpt.getContext("2d");
               var rtmpt = '室温';
               rtmpt_ctx.beginPath();
               //風速 タイトル
               var draw_airS = document.getElementById("canvas_O");
               var airS_ctx = draw_airS.getContext("2d");
               var airS = '風速';
               airS_ctx.beginPath();
               //推奨温度 タイトル
               var draw_coTmp = document.getElementById("canvas_O");
               var coTmp_ctx = draw_coTmp.getContext("2d");
               var coTmp = '推定温度(15分毎)';
               coTmp_ctx.beginPath();
               //室温 数値
               var draw_tmp = document.getElementById("canvas_O");
               var tmpv_ctx = draw_tmp.getContext("2d");
               var temp = getTemp();
               var tmpTxt = temp+'℃';
               tmpv_ctx.beginPath();
               //風速 数値
               var draw_airP = document.getElementById("canvas_O");
               var airP_ctx = draw_airP.getContext("2d");
               //var airP = getTemp();
               var airP = '弱';
               airP_ctx.beginPath();
               //推奨温度 数値
               var draw_coTmpv = document.getElementById("canvas_O");
               var coTmpv_ctx = draw_coTmpv.getContext("2d");
               var coTmpv = getCTemp();
               var ctTxt = coTmpv +'℃';
               coTmpv_ctx.beginPath();
            //******************************************
            //**************** 枠組み 表示 ********************
                // 四角を描く
               //モニターの外枠　
               rect_ctxB.fillStyle = "rgb(100,100,100)";
               rect_ctxB.fillRect(5, 20, 450, 300);
              //モニターの画面
               rect_ctxF.fillStyle = "rgb(168,239,175)";
               rect_ctxF.fillRect(30, 45, 400, 250);
               //枠 横上
               rect_frameA_ctx.strokeStyle = "rgb(0,0,0)";
               rect_frameA_ctx.lineWidth = 3;
               rect_frameA_ctx.strokeRect(31, 100, 398, 65);
               //枠 横下
               rect_frameU_ctx.lineWidth = 3;
               rect_frameU_ctx.strokeStyle = "rgb(0,0,0)";
               rect_frameU_ctx.strokeRect(31, 165, 398, 65);
               //枠　縦
               rect_frameV_ctx.lineWidth = 3;
               rect_frameV_ctx.strokeStyle = "rgb(0,0,0)";
               rect_frameV_ctx.strokeRect(180,100,10 ,130);
            //****************** 数値　表示 *******************
              //室温　タイトル
               rtmpt_ctx.font = "italic 55px Arial";
               rtmpt_ctx.fillStyle = "black";
               rtmpt_ctx.fillText(rtmpt, 50, 150,100);
               //推奨温度 タイトル
               coTmp_ctx.font = "italic 55px Arial";
               coTmp_ctx.fillStyle = "black";
               coTmp_ctx.fillText(coTmp, 200, 150,200);
               //室温 数値
               tmpv_ctx.font = "italic 55px Arial";
               tmpv_ctx.fillStyle = "black";
               tmpv_ctx.fillText(tmpTxt, 30, 220,130);
               //推奨温度 数値
               coTmpv_ctx.font = "italic 55px Arial";
               coTmpv_ctx.fillStyle = "black";
               coTmpv_ctx.fillText(ctTxt, 215, 220,180);
           }
        </script>
    ~~~
