#include <AccelStepper.h>

// ピン設定
#define STEP_PIN  12   // ステップ信号用のピン
#define DIR_PIN   14   // 方向制御用のピン

// AccelStepper のインスタンスを作成（DRIVER モード）
AccelStepper stepper(AccelStepper::DRIVER, STEP_PIN, DIR_PIN);
String receivedData = "";  // 受信データのバッファ

void setup() {
    Serial.begin(9600);
    stepper.setMaxSpeed(3000);  // 高音にも対応できるようにする
    stepper.setSpeed(0);  // 初期速度
}

void loop() {
    stepper.runSpeed();  // 速度を維持して回転

    // シリアルデータ受信
    while (Serial.available()) {
        char c = Serial.read();
        if (c == '\n') {  
            float frequency = receivedData.toFloat(); // 数値に変換
            stepper.setSpeed(frequency);  // 速度変更
            Serial.print("Set Speed: ");
            Serial.print(frequency);
            Serial.println(" Hz");
            receivedData = "";  // バッファをクリア
        } else {
            receivedData += c;
        }
    }
}