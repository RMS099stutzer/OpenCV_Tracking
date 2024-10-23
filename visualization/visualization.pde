import processing.net.*;
import javax.swing.JOptionPane;
import java.awt.Point;

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

int currentState = 0;

void setup() {
    fullScreen(P3D);
    stroke(0);
    hint(ENABLE_DEPTH_SORT);
    lights();
    
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
    
    if (currentState == 0) {    // Start screen
        displayStartScreen();
    } else if (currentState == 1 || currentState == 2) { // Visualization screen
        setCameraRotation();
        renderLines();
        handleClientMessage();
    } else if (currentState == 3) { // Exit
        exit();
    } else if (currentState == 5) { // End screen
        elapsedTime = millis() - baseTime;
        displayEndScreen();
        handleEndScreenState();
    }
}