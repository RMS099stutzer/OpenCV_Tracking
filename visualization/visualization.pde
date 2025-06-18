import processing.net.*;
import javax.swing.JOptionPane;
import java.awt.Point;

StateManager stateManager;
EndScreenState endScreenState;
StraightLine straightLine;

Server server;
String clientMessage;

int isFirstReceive = 0;

final int PORT = 10001;
final int MAX_LINES = 10000;
final int OUTLIER_VALUE = 9999;

PVector[] start = new PVector[MAX_LINES];
PVector[] end = new PVector[MAX_LINES];

int baseTime = 0;
int elapsedTime;

//int currentState = 0;

void setup() {
    fullScreen(P3D);
    stroke(0);
    hint(ENABLE_DEPTH_SORT);
    lights();
    stateManager = new StateManager();
    endScreenState = new EndScreenState();
    straightLine = new StraightLine();

    frameRate(60);
    
    server = new Server(this, PORT);
    println("server address: " + server.ip());
    
    initializeValues();
    
    textSize(54);
    textFont(createFont("ＭＳ ゴシック", 48, true));
}

void draw() {
    background(255);
    translate(width / 2, height / 2, 0);
    stateManager.current();
}