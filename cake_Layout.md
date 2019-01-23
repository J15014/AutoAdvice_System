# レイアウト

#### 概要
Web確認画面のレイアウトについて記載　　　

主にCSS, JavaScriptファイルについて


####  ・変更・追加した点
-  CSS
- JavaScript
- その他


## CSS

- ヘッダーの設定
 ~~~
 header{

   padding: 10px;
   background-color: #purple;
 }
~~~

- 画面端に畳まれているナビゲーションドロワーの内での設定
    ~~~
    ##ナビゲーションドロワー内のテーブルの背景色などの設定
    #nav-drawer{
        position: relative;
    }

    .nav-unshown{
        display: none;
    }

    .nav-table tr{
        background-color: #9999ff;
    }

    .nav-table th{
        text-align: center;
        border: none;
    }

    .nav-table td{
        align-items: center;
    }

    ##　テーブル内のボタンの大きさ・色等の設定

    .nav-table .btnOn, .btnOff, .btnR, .btnO{
        width: 49%;
    }

    .nav-table .btnOn{
        color: #ff0099;
    }
    .nav-table .btnOff{
        color: #000000;
    }

    .nav-table .btnR{
        color: #00aa33;
    }

    .nav-table .btnO{
        color: #7CC2DD;
    }

    ## ナビゲーションドロワー内のテーブルの設定
    .nav-table p{
        font-style:oblique;
        font-size: 20px;
        text-align: center;
        margin: auto;
        width: 330px;
    }

    ##ボタンへの設定
    ##メニューボタンが常に画面最前列に来るように調整
    #chart_divTe{
        z-index: 900;
    }

    #chart_divO{
        z-index: 900;
    }

    #chart_divHu{
        z-index: 900;
    }

    ##ドロワー内メニューの表示時の色、大きさ等
    #nav-open, #nav-open span{
        display: inline-block;
        box-sizing: border-box;
        position: fixed;
        z-index: 9999;
        transition: .3s ease-in-out;
        -webkit-transform: translate(0%, 0%);
        transform: translate(0%, 0%);
    }

    #nav-open{
        width: 30px;
        height: 25px;
    }

    ##ドロワーを開くためのアイコンの設定
    #nav-open span{
        position: absolute;
        left: 0;
        width: 100%;
        height: 4px;
        border-radius: 2px;
    }

    #nav-open span:nth-of-type(1){
         top: 0;
         background-color: #8b0000;
    }

    #nav-open span:nth-of-type(2){
         top: 10px;
         background-color: #2e8b57;
    }

    #nav-open span:nth-of-type(3){
         bottom: 0;
         background-color: #4b0082;
    }

    ##普段隠されている時の設定
    #nav-close{
        display: none; /*はじめは隠しておく*/
        position: fixed;
        z-index: 99;
        top: 0; /*全体に広がるように*/
        left: 0;
        width: 100%;
        height: 100%;
        background: skyblue;
        opacity: 0;
        transition: .3s ease-in-out;
    }

    ##メニューの展開動作等
    /*中身*/
    #nav-content{
        overflow: auto;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 9800; /*最前面に*/
        /* max-width: 330px;/*最大値 */
        height: 100%;
        background-color: #307 ; /*背景色*/
        transition: .3s ease-in-out; /*なめらかに表示*/
        -webkit-transform: translateX(-105%);
        transform: translateX(-105%);
    }

    ##アイコンがクリックされた時の動作を決めている
    #nav-input:checked ~ #nav-close {
        display: block;
        opacity: .5;
    }

    #nav-input:checked ~ #nav-content{
        -webkit-transform: translateX(0%);
        transform: translateX(0%);
        box-shadow: 6px 0 25px rgba(0, 0, 0, .15);
    }

    #nav-input:checked ~ #nav-open {
        transition: .3s ease-in-out;
        transform: translate(0%, -160%);
    }

    ## 上の線を上に上げて斜めにする
    #nav-input:checked ~ #nav-open span:nth-of-type(1) {
        transform: translateY(30px) rotate(-45deg);
    }

    ## 真ん中の線をフェードアウトさせる
    #nav-input:checked ~ #nav-open span:nth-of-type(2) {
        opacity: 0;
    }

    ## 下の線を上に上げて斜めにする
    #nav-input:checked ~ #nav-open span:nth-of-type(3) {
        transform:translate(3%) translateY(10px) rotate(45deg);
    }

    ~~~
    - transform:translateを用いてアイコンの位置・角度を変えるように設定している。

## JavaScript　ファイル
- 主にナビゲーションドロワー内のボタンを押した時の動作について設定している。
~~~
    $(function(){
        var showFlg = 0;

        ##スマートフォン等の端末毎にボタンの大きさを変える処理
        var ua = navigator.userAgent;
        if (ua.indexOf('iPhone') > 0 || ua.indexOf('Android') > 0 && ua.indexOf('Mobile') > 0) {
            // スマートフォン用コード
            $('html').css('font-size','150%').css('max-width','wrap-content').css('width', 'wrap-content');
            $('input').css('transform','scale(1.0)').css('margin','0.5em');
            $('.nav-table .btnOn, .btnOff, .btnO, .btnR').css('width', '40%').css('font-size', '80%');
            $('#chart_divO, #chart_divTe', '#chart_divO').css('width', 'wrap-content');
            $('#nav-content').css('width', '100%');
            $('#nav-input:checked ~ #nav-open').css('transform',  'translate(0%, -160%)');
        } else if (ua.indexOf('iPad') > 0 || ua.indexOf('Android') > 0) {
            // タブレット用コード
            $('html').css('font-size','150%');
            $('input').css('transform','scale(1.2)').css('margin','0.5em');
        } else {
        // PC用コード
            $('.nav-table .btnOn, .btnOff, .btnO, .btnR').css('width', '49%').css('font-size', '200%');
        }

        ##外気温のグラフを初期状態では非表示に
        $('#chart_divO').css('visibility', 'hidden');

        ##ボタンが押された時に最後に室内・外気のどちらを表示していたからを判別してグラフを表示する
        $('.btnOn').on('click',function(){
            if(showFlg == 0){
                $('#chart_divTe').css('visibility', 'visible');
                $('#chart_divHu').css('visibility', 'visible');
                $('#chart_divO').css('visibility', 'hidden');
                $("html,body").animate({scrollTop:$('#chart_divTe').offset().top});
            } else {
                $('#chart_divTe').css('visibility', 'hidden');
                $('#chart_divHu').css('visibility', 'hidden');
                $('#chart_divO').css('visibility', 'visible');
                $("html,body").animate({scrollTop:$('#chart_divO').offset().top});
            }
        });

        ##ボタンが押されたらグラフを非表示にする
        $('.btnOff').on('click',function(){
            $('#chart_divTe').css('visibility', 'hidden');
            $('#chart_divO').css('visibility', 'hidden');
            $('#chart_divHu').css('visibility', 'hidden');
        });

        ##こちらが押された場合は室内のグラフを表示する
        $('.btnR').on('click', function(){
            showFlg = 0;
            $('#chart_divTe').css('visibility', 'visible');
            $('#chart_divHu').css('visibility', 'visible');
            $('#chart_divO').css('visibility', 'hidden');
            $("html,body").animate({scrollTop:$('#chart_divTe').offset().top});
        });

        ##こちらが押された場合は外気のグラフを表示する
        $('.btnO').on('click', function(){
            showFlg = 1;
            $('#chart_divTe').css('visibility', 'hidden');
            $('#chart_divHu').css('visibility', 'hidden');
            $('#chart_divO').css('visibility', 'visible');
            $("html,body").animate({scrollTop:$('#chart_divO').offset().top});
        });
    });
    ~~~

### その他
- cakephpフォルダ内のapp/View/Layouts/のdefault.ctpを編集して、cakephpデフォルトのヘッダー・フッターの不要な部分を削除した。
