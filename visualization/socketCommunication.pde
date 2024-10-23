int receivedLines;

void handleClientMessage() {
    elapsedTime = millis() - baseTime;
    Client client = server.available();
    if (client == null) {
        return;
    }
    clientMessage = client.readString();
    String[] messageParts = split(clientMessage, ',');
    if (unhex(messageParts[0]) == 43690) {
        start[lineCount] = new PVector(0, 0, 0);
        isFirstReceive = 0;
    }
    if (unhex(messageParts[0]) == 65535) {
        if (isFirstReceive == 0) {
            start[lineCount] = new PVector(int(messageParts[1]), int(messageParts[2]), int(messageParts[3]));
            isFirstReceive = 1;
        } else {
            end[lineCount] = new PVector(int(messageParts[1]), int(messageParts[2]), int(messageParts[3]));
            start[lineCount + 1] = end[lineCount];
            lineCount++;
            receivedLines++;
        }
        baseTime = millis();
    }
    if (currentState == 2) {
        end[lineCount] = new PVector(int(messageParts[1]), int(messageParts[2]), int(messageParts[3]));
        lineCount++;
        receivedLines++;
        csvFile = createWriter("csv/" + year() + nf(month(), 2) + nf(day(), 2) + nf(hour(), 2) + nf(minute(), 2) + nf(second(), 2) + ".csv");
        createCSVFile();
        currentState = 5;
    }
    remainingSeconds = 5;
}