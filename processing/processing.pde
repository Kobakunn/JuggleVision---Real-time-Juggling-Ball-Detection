import oscP5.*;
import netP5.*;

OscP5 oscP5;

// =========================
// 設定
// =========================

final int MAX_BALLS = 3;
ArrayList<Particle> particles = new ArrayList<Particle>();
ArrayList<Trail> trails = new ArrayList<Trail>();


// =========================
// ボール情報
// =========================

int[] ballID = new int[MAX_BALLS];

float[] ballX = new float[MAX_BALLS];
float[] ballY = new float[MAX_BALLS];

float[] ballWidth = new float[MAX_BALLS];
float[] ballHeight = new float[MAX_BALLS];

float[] confidence = new float[MAX_BALLS];

int ballCount = 0;


// =========================
// エフェクト設定
// =========================

boolean effectEnabled = true;


void setup() {
  size(640, 640);
  oscP5 = new OscP5(this, 8000);
}


void draw() {
  background(10);

  // =========================
  // 残像
  // =========================

  for (int i = trails.size() - 1; i >= 0; i--) {

    Trail t = trails.get(i);

    t.update();
    t.display();

    if (t.dead()) {
      trails.remove(i);
    }
  }


  // =========================
  // パーティクル
  // =========================

  for (int i = particles.size() - 1; i >= 0; i--) {

    Particle p = particles.get(i);

    p.update();
    p.display();

    if (p.dead()) {
      particles.remove(i);
    }
  }


  // =========================
  // ボール
  // =========================

  for (int i = 0; i < ballCount; i++) {

    drawBallEffect(i);

  }


  // =========================
  // 情報表示
  // =========================

  fill(255);
  textSize(20);

  text(
    "Balls: " + ballCount,
    20,
    30
  );
}


// =========================
// ボールエフェクト
// =========================

void drawBallEffect(int index) {

  float x = ballX[index];
  float y = ballY[index];

  float size =
    max(
      ballWidth[index],
      ballHeight[index]
    );

  // =========================
  // 残像を生成
  // =========================

  if (effectEnabled) {

    trails.add(
      new Trail(
        x,
        y,
        size
      )
    );

  }


  if (effectEnabled) {
    if (random(1) < 0.6) {
      float angle = random(TWO_PI);
      float speed = random(0.5, 2.0);
      particles.add(
        new Particle(
          x,
          y,
          cos(angle) * speed,
          sin(angle) * speed,
          size * 0.12
        )
      );
    }
  }


  // -------------------------
  // 光
  // -------------------------

  if (effectEnabled) {

    noStroke();


    // 外側の光

    fill(80, 208, 255, 20);

    ellipse(
      x,
      y,
      size * 3.0,
      size * 3.0
    );


    // 中間の光

    fill(80, 208, 255, 40);

    ellipse(
      x,
      y,
      size * 2.2,
      size * 2.2
    );


    // 内側の光

    fill(80, 208, 255, 80);

    ellipse(
      x,
      y,
      size * 1.5,
      size * 1.5
    );

  }


  // -------------------------
  // ボール
  // -------------------------

  fill(255);

  noStroke();

  ellipse(
    x,
    y,
    ballWidth[index],
    ballHeight[index]
  );


  // -------------------------
  // ID
  // -------------------------

  fill(255);

  textSize(16);

  text(
    "ID: " + ballID[index],
    x + size,
    y
  );

}


// =========================
// OSC受信
// =========================

void oscEvent(OscMessage message) {

  if (
    message.checkAddrPattern("/balls")
  ) {

    ballCount =
      message.get(0).intValue();


    ballCount =
      min(
        ballCount,
        MAX_BALLS
      );


    for (int i = 0; i < ballCount; i++) {
      int index = 1 + i * 6;

      ballID[i] =
        message
          .get(index)
          .intValue();

      ballX[i] =
        message
          .get(index + 1)
          .floatValue();

      ballY[i] =
        message
          .get(index + 2)
          .floatValue();

      ballWidth[i] =
        message
          .get(index + 3)
          .floatValue();

      ballHeight[i] =
        message
          .get(index + 4)
          .floatValue();

      confidence[i] =
        message
          .get(index + 5)
          .floatValue();
    }
  }
}

class Particle {
  float x;
  float y;

  float vx;
  float vy;

  float life;

  float size;


  Particle(
    float x,
    float y,
    float vx,
    float vy,
    float size
  ) {
    this.x = x;
    this.y = y;

    this.vx = vx;
    this.vy = vy;

    this.life = 255;

    this.size = size;
  }

  void update() {
    x += vx;
    y += vy;

    life -= 5;
  }

  void display() {
    noStroke();

    fill(
      173,
      216,
      230,
      life
    );

    ellipse(
      x,
      y,
      size,
      size
    );
  }

  boolean dead() {
    return life <= 0;
  }
}


class Trail {

  float x;
  float y;

  float size;

  float life;


  Trail(
    float x,
    float y,
    float size
  ) {

    this.x = x;
    this.y = y;

    this.size = size;

    this.life = 180;
  }


  void update() {
    life -= 3;
  }


  void display() {

    noStroke();

    fill(
      80,
      208,
      255,
      life
    );

    ellipse(
      x,
      y,
      size,
      size
    );

  }


  boolean dead() {
    return life <= 0;
  }

}