import processing.net.*;    //processingソケット通信
import processing.net.*;    //processingソケット通信
// import gifAnimation.*;      //(extrapixel/gif-animation at 3.0)をダウンロードし解凍してprocessingのlibrariesフォルダにgifAnimationをコピー
import javax.swing.JOptionPane;
import java.awt.Point;

// GifMaker gifExport;
final int NUMBER = 24;

int port = 10001;           //適当なポート番号(受信、送信で一致させる)
Server server;              //Server型

int base_time = 0;          //一定時間ごとにmillis()を初期化
int base_time1 = 0;
int base_time2 = 0;
int base_time3 = 0;

int NUM = 10000;            //描ける直線の総数
int i;                      //直線の数
PVector[] start = new PVector[NUM];     //直線の始まりの座標
PVector[] end = new PVector[NUM];       //直線の終わりの座標
int ln;                     //受信した行数
float xx;                   //{
float zz;                   //
float px, pz;               //
float rotX,rotY,protY;      //マウスで座標を記録する値
float xc, yc, zc;           //
float pxc, pyc, pzc;        //}
float s;                    //拡大サイズ
PrintWriter file;           //書き込む型
int jump = 9999;            //csvファイルの外れ値
int head = 0;               //受信が1回目のとき
int head1 = 0;
int ap = 2;                 //5秒待つ
int sele = 0;               
int time;                   //時間
int time1;
int time2;
int time3;
int time_sele;
String whatClientSaid;      //受信する型
int count;                  //これまで繰り返した数
float msg_X;
float msg_Y;
float msg_speedX;
float msg_speedY;
int clickX;
int clickY;
float pull_X;
float pull_Y;
int dragging = 0;
float strong;
int load;
int load_counter;
int finish_msg;
int load_meter;
float bound0;
float bound1;
float bound2;
int bound_sele;
int finish;
int final_error_msg;


void setup() {
    // size(1366, 768, P3D);           //横1366，縦768の3D
    fullScreen(P3D);                //フルスクリーン
    stroke(0);                      //線の色(白色)
    hint(ENABLE_DEPTH_SORT);        //P3DレンダラとOPENGLレンダラにおいて、プリミティブなzソートを有効にする．(よく分からん)
    lights();                       //デフォルトの環境光
    textSize(54);                   //テキストサイズを54
    frameRate(60);                  //フレームレートを30
    server = new Server(this, port);
    println("server address: " + server.ip());      //このパソコンのIPアドレスを表示
    formatting();                   //いろいろな数値を初期化
    count = 0;
    
    textFont(createFont("ＭＳ ゴシック", 48, true));             //フォントをMS明朝にする．
}

void draw() {
    background(255);                        //背景を白にする
    translate(width / 2, height / 2,0);         //中心を決定
    if (sele == 3) {
        exit();         //強制終了
    }
    // else if (sele == 4) {
    //     errorscreen1();
// }
    else if (sele == 5) {
        time = millis() - base_time;        //時間を初期化
        endscreen1();
        if (finish_msg == 1) {
            if (time >= 1000) {      //1秒待つ
                base_time = millis();
                ap--;
            }
            if (ap == 0) {
                sele = 0;       //初期画面に戻す
                for (int k = 0; k < i; k++) {
                    start[k] = new PVector(0,0,0);      //配列を初期化
                    end[k] = new PVector(0,0,0);        //同上
                }
                formatting();
            }
        }
    }
    else if (sele == 1 || sele == 2) {
        if (sin(zz) >= 0) {
            camera(500 * cos(xx) * sin(zz), 500 * sin(xx) * sin(zz), 500 * cos(zz), xc, yc, 0, 0, 0, -1);
        }           //カメラの位置
        else {
            camera(500 * cos(xx) * sin(zz), 500 * sin(xx) * sin(zz), 500 * cos(zz), xc, yc, 0, 0, 0, 1);
        }           //カメラの位置
        
        stroke(0);
        rotateX(0);
        rotateY(0);
        scale(s);
        textAlign(CENTER); // x方向をセンタリング，y方向の座標はベースライン
        text("X", 200, 0, 0); // XY平面上に書く
        text("Y", 0, 200, 0); // XY平面上に書く 
        text("Z", 0, 0, 200); // Z=200のXY平面上に書く
        strokeWeight(1);
        line(0, 0, 0, 160, 0, 0); // X軸
        line(0, 0, 0, 0, 160, 0); // Y軸
        line(0, 0, 0, 0, 0, 160); // Z軸
        
        
        strokeCap(ROUND);
        strokeWeight(10);
        
        for (int k = 0; k < i; k++) {
            stroke(0);
            strokeWeight(10);
            // 線を描く
            line(start[k].x, start[k].y, start[k].z, end[k].x, end[k].y, end[k].z);
        }
        
        //毎フレームごとに線を描く
        
        time = millis() - base_time;        //一定時間ごとにtimeを初期化
        Client client = server.available(); //clientに受信した信号を受け取る
        if (client ==  null) {          
            return;             //最初に戻る
        }
        else{
            //何もしない
        }
        whatClientSaid = client.readString();       //受信した文字列を収容
        String[] so = split(whatClientSaid, ',');   //コンマで区切られた文字列を分ける
        if (unhex(so[0]) == 43690) {                 //AAAAならば
            start[i] = new PVector(0,0,0);
            head = 0;
            // return;
        }
        if (unhex(so[0]) == 65535) {       //so[0]がFFFFなら
            if (head == 0) {          //1回目かAAAAの次
                start[i] = new PVector(int(so[1]),int(so[2]),int(so[3]));
                head = 1;
            }
            else{
                end[i] = new PVector(int(so[1]),int(so[2]),int(so[3]));
                start[i + 1] = end[i];  //終端と先端を一致させる
                i++;
                ln++;       //1行増やす
            }
            base_time = millis();
        }
        
        
        if (sele == 2) {
            end[i] = new PVector(int(so[1]),int(so[2]),int(so[3]));
            i++;
            ln++;
            file = createWriter("csv/test_" + count + ".csv");  //csvファイルを順次作成
            makecsvfile();
            sele = 5;
            count++;
        }
        ap = 5;
    }
    else if (sele == 0) {
        startscreen();
        //base_time1 = millis();
        //base_time2 = millis();
        //sele = 5;
    }
}
void mouseDragged() {            //マウスの割り込み
    if (mouseButton == LEFT) {
        if (mouseX - pmouseX >= 0) {
            xx = map(mouseX - pmouseX, 0, width, 0, 2 * PI);
        }
        if (mouseX - pmouseX <= 0) {
            xx = map(mouseX - pmouseX, -width, 0, -2 * PI, 0);
        }
        xx += px;
        px = xx;
        
        if (mouseY - pmouseY >= 0) {
            zz = map(mouseY - pmouseY, 0, height, 0, 2 * PI);
        }
        if (mouseY - pmouseY <= 0) {
            zz = map(mouseY - pmouseY, -height, 0, -2 * PI, 0);
        }
        zz += pz;
        pz = zz;
    }
    
    if (mouseButton == CENTER) {      //平行移動
        xc += pmouseY - mouseY;
        pxc = xc;
        yc += mouseX - pmouseX;
        pyc = yc;
    }
}

void mouseWheel(MouseEvent e) {      //ホイールでサイズを変更
    float mw = e.getCount();
    if (mw == 1) {
        s *= 0.9;
    }
    if (mw == -1) {
        s *= 1.1;
    }   
}

void mousePressed() {
    pull_X = mouseX;
    pull_Y = mouseY;
    clickX++;
    clickY++;
    dragging = 1;
}

void mouseReleased() {
    msg_speedX = (pull_X - mouseX) * 0.5;
    msg_speedY = (pull_Y - mouseY) * 0.5;
    dragging = 0;
}


void keyPressed() {          //キーを押したら
    if (key == ENTER) {
        sele = 1;
    }
    else if (key == TAB) {
        base_time1 = millis();
        base_time2 = millis();
        finish = 1;
        sele = 2;
    }
    else if (key == ESC) {
        sele = 3;
    }
    else {
        sele = 0;
    }
}

void formatting() {          //初期化
    head = 0;
    head1 = 0;
    i = 0;
    ln = 0;             //行数を0にする
    px = PI / 6;          //
    pz = PI / 6;          //
    xx = PI / 6;          //
    zz = PI / 6;          //カメラの初期環境
    xc = 0;             //
    yc = 0;             //
    zc = 0;             //
    s = 1.2;            //
    msg_speedX = 5;
    msg_speedY = 3;
    msg_X = 0;
    msg_Y = 0;
    clickX = 0;
    clickY = 0;
    time_sele = 50;
    load = 0;
    load_counter = 4;
    load_meter = 0;
    finish_msg = 0;
    ap = 2;
    bound0 = 0;
    bound1 = 0;
    bound2 = 0;
    bound_sele = 0;
    finish = 0;
    strokeWeight(1);
}

void makecsvfile() {         //csvファイルの作成
    file.println(start[0].x + "," + start[0].y + "," + start[0].z);
    file.flush();
    for (int o = 0; o < ln - 1; o++) {
        if (start[o + 1].x == end[o].x && start[o + 1].y == end[o].y && start[o + 1].z == end[o].z) {//終端と先端が一致するなら
            file.println(start[o + 1].x + "," + start[o + 1].y + "," + start[o + 1].z);
            file.flush();
        }
        else {
            file.println(end[o].x + "," + end[o].y + "," + end[o].z);
            file.println(jump + "," + jump + "," + jump);       //外れ値を出力
            file.println(start[o + 1].x + "," + start[o + 1].y + "," + start[o + 1].z);
            file.flush();
        }
    }
    file.println(end[ln - 1].x + "," + end[ln - 1].y + "," + end[ln - 1].z);
    file.flush();
    file.close();
}

void startscreen() {         //初期画面
    camera(0,10,500, 0, 0, 0, 0, 0, -1);
    hint(DISABLE_DEPTH_TEST);
    fill(0);
    // textFont(createFont("HG正楷書体-PRO", 110));
    textSize(54);
    text("ENTERキーを押して",0, 0);
    textAlign(CENTER,CENTER);
    hint(ENABLE_DEPTH_TEST);  // z軸を有効化
}

void startscreen1() {         //画面バウンド
    camera(0,10,500, 0, 0, 0, 0, 0, -1);
    hint(DISABLE_DEPTH_TEST);
    fill(0);
    textSize(54);
    
    //msg_speedX *=0.99;
    //msg_speedY *=0.99;
    
    msg_X += msg_speedX;
    msg_Y += msg_speedY;
    if (msg_X - 415 < - width / 2 || msg_X + 410 > width / 2) {
        msg_speedX *= -1;
    }
    if (msg_Y - 100 < - height / 2 || msg_Y + 115 > height / 2) {
        msg_speedY *= -1;
    }
    textAlign(CENTER,CENTER);
    text("ENTERキーを押して",msg_X, msg_Y);
    
    if (dragging == 1) {
        stroke(255,0,0);
        float angle = atan2(mouseY - pull_Y,mouseX - pull_X);
        //float strong = sqrt(sq((pull_X - width / 2) + (mouseX- width / 2)) + sq((pull_Y - height / 2) + (mouseY- height / 2)))*0.1;
        strong = dist(pull_X,pull_Y,mouseX,mouseY) / 4;
        line(pull_X - width / 2,pull_Y - height / 2,mouseX - width / 2,mouseY - height / 2);
        translate(pull_X - width / 2, pull_Y - height / 2);
        rotate(angle);
        //line(0,0,5,2.5);
        //line(0,0,5,-2.5);
        line(0,0, strong + 3,(strong) / 4);
        line(0,0, strong + 3, -(strong) / 4);
    }
    stroke(0);
    hint(ENABLE_DEPTH_TEST);  // z軸を有効化
}

void endscreen() {           //終了画面
    camera(0, 10, 500, xc, yc, 0, 0, 0, -1);
    background(255);
    hint(DISABLE_DEPTH_TEST);
    fill(0);
    // textFont(createFont("HG正楷書体 - PRO", 110));
    textSize(54);
    text("終了まであと",200, 220);
    text(ap,380, 220);
    text("秒",430, 220);
    textAlign(CENTER,CENTER);
    hint(ENABLE_DEPTH_TEST);  // z軸を有効化
}

void endscreen1() {           //終了画面
    time1 = millis() - base_time1;
    time2 = millis() - base_time2;
    camera(0, 10, 500, xc, yc, 0, 0, 0, -1);
    background(255);
    hint(DISABLE_DEPTH_TEST);
    noFill();
    rect(100,230,400,20);
    if (load == 1) {
        fill(0,0,255);
        rect(100,230,load_meter,20);
        if (load_meter == 80) {
            time_sele = 500;
            load_counter = 40;
        }
        else if (load_meter == 120) {
            load_counter = 120;
        }
        else if (load_meter == 360) {
            load_counter = 36;
        }
        else if (load_meter == 396) {
            time_sele = 1000000000;
            finish_msg = 1;
            base_time = millis();
            load = 2;
        }
    }
    else if (load == 2) {
        fill(0,0,255);
        rect(100,230,load_meter,20);
    }
    
    if (time1 > time_sele) {
        base_time1 = millis();
        load_meter += load_counter;
        load = 1;
    }
    fill(0);
    //textFont(createFont("HG正楷書体-PRO", 110));
    textSize(30);
    text("送信中",220,210);
    text(".",272,212 + ( -10 * abs(sin(bound0 + PI))));
    text(".",292,212 + ( -10 * abs(sin(bound1 + PI))));
    text(".",312,212 + ( -10 * abs(sin(bound2 + PI))));
    if (time2 > 10) {
        if (bound_sele == 0) {
            bound0 += 0.1;
            base_time2 = millis();
            if (bound0 >= 3) {
                bound0 = 0;
                bound_sele = 1;
            }
        }
        else if (bound_sele == 1) {
            bound1 += 0.1;
            base_time2 = millis();
            if (bound1 >= 3) {
                bound1 = 0;
                bound_sele = 2;
            }
        }
        else if (bound_sele == 2) {
            bound2 += 0.1;
            base_time2 = millis();
            if (bound2 >= 3) {
                bound2 = 0;
                bound_sele = 0;
            }
        }
    }
    textAlign(LEFT,CENTER);
    text("(" + int(((load_meter / 4) * 10.34)) + "/1024)",320,210);
    textAlign(CENTER,CENTER);
    textSize(54);
    if (finish_msg == 1) {
        //text("初期化まであと" + ap + "秒",0, 0);
    }
    else {
        //gif();
    }
    hint(ENABLE_DEPTH_TEST);  // z軸を有効化
}

void errorscreen1() {
    // background(255);
    // camera(0,10,500, 0, 0, 0, 0, 0, -1);
    // hint(DISABLE_DEPTH_TEST);
    // fill(0);
    // //textFont(createFont("HG正楷書体-PRO", 110));
    // textSize(54);
    // textAlign(CENTER,CENTER);
    // //text("あ",100,100);
    // text("何も受信してないのにcsvに書き込もうと  するな!!      初期化しろ", -260, -300,560,600);
    // time3 = millis() -  base_time3;
    // resetMatrix();
    // if (head1 == 0) {
    //     showErrorDialogs("Microsoft Windows", "Windows was not installed correctly. Please reinstall Windows.\nError 4(Windows error 2021D)", 8500, 74, 50); // 74個のエラーメッセージを0.05秒ごとに表示
    //     head1 = 1;
// }
    // if (time3 > 12000) {
    //     sele = 0;
// }
    // hint(ENABLE_DEPTH_TEST);  // z軸を有効化
}

void showErrorDialogs(String title, String message, int totalDuration, int error_num, int interval) {
    new Thread(new Runnable() {
        public void run() {
            javax.swing.JDialog[] dialogs = new javax.swing.JDialog[error_num];
            int startX = 0;
            int startY = 100;
            int offsetX = 20;
            int offsetY = 20;
            for (int error_count = 0; error_count < error_num; error_count++) {
                final_error_msg = error_count;
                if (error_count >= 25) {
                    offsetY = ((error_count - 25) * 20) - 50;
                    offsetX = ((error_count - 25) * 20) + 250;
                    if (error_count > 51) {
                        offsetY = ((error_count - 51) * 20) - 100;
                        offsetX = ((error_count - 51) * 20) + 500;
                    }
                }
                else{
                    offsetY = error_count * 20;
                    offsetX = error_count * 20;
                }
                final int index = error_count;
                final int x = startX + offsetX;
                final int y = startY + offsetY;
                javax.swing.SwingUtilities.invokeLater(new Runnable() {
                    public void run() {
                        if (final_error_msg ==  73) {
                            JOptionPane pane = new JOptionPane("重大なエラーが発生しました\n10秒後に初期化します", JOptionPane.WARNING_MESSAGE);
                            dialogs[index] = pane.createDialog(title);
                            dialogs[index].setModal(false); // 非モーダルに設定
                            dialogs[index].setAlwaysOnTop(true); // ダイアログを最前面に設定
                            dialogs[index].setVisible(true);
                        }
                        else {
                            JOptionPane pane = new JOptionPane(message, JOptionPane.ERROR_MESSAGE);
                            dialogs[index] = pane.createDialog(title);
                            dialogs[index].setModal(false); // 非モーダルに設定
                            dialogs[index].setAlwaysOnTop(true); // ダイアログを最前面に設定
                            dialogs[index].setLocation(x,y); // ダイアログの位置を設定
                            dialogs[index].setVisible(true);
                        }
                    }
                });
                try {
                    Thread.sleep(interval); // 次のダイアログを表示するまで待機
                } catch(InterruptedException e) {
                    e.printStackTrace();
                }
            }
            try {
                Thread.sleep(totalDuration); // 全てのダイアログを表示した後、指定された時間待機
            } catch(InterruptedException e) {
                e.printStackTrace();
            }
            for (javax.swing.JDialog dialog : dialogs) {
                if (dialog != null) {
                    dialog.dispose(); // 全てのダイアログを閉じる
                }
            }
        }
    }).start();
}

void gif () {
    // for(int i = 0; i < NUMBER; i++){
    //     float angle = i * 2*PI / NUMBER;
    //     float v = pow(abs(sin(angle / 2 + frameCount * 0.03)), 4);
    //     float r = map(v, 0, 1, 10, 20);
    //     fill(0,0,0);
    //     ellipse((150 + r) * cos(angle),(150 + r) * sin(angle), r * 2, r * 2);
// }
    // if(frameCount <= 50*3){
    //  // gifExport.addFrame();
// }
    // else {
    //     // gifExport.finish();
// }
}