/**
 * HireSense AI — Cursor-reactive canvas wave background
 * 7 layers, misty white to deep navy
 */
(function() {
  var canvas = document.getElementById('waveCanvas');
  if (!canvas) return;
  var ctx = canvas.getContext('2d');
  var w = 0, h = 0;
  var mouseX = -1, mouseY = -1;
  var layers = [
    { color: 'rgba(220, 240, 248, 0.9)', speed: 0.0008, amp: 18, yOffset: 0.15 },
    { color: 'rgba(180, 225, 238, 0.85)', speed: 0.0006, amp: 22, yOffset: 0.28 },
    { color: 'rgba(120, 200, 220, 0.85)', speed: 0.0007, amp: 26, yOffset: 0.42 },
    { color: 'rgba(70, 160, 190, 0.9)', speed: 0.0005, amp: 30, yOffset: 0.56 },
    { color: 'rgba(30, 110, 150, 0.9)', speed: 0.0006, amp: 34, yOffset: 0.70 },
    { color: 'rgba(15, 70, 105, 0.95)', speed: 0.0004, amp: 38, yOffset: 0.84 },
    { color: 'rgba(5, 30, 55, 1)', speed: 0.0003, amp: 42, yOffset: 1 }
  ];
  function resize() {
    w = canvas.width = window.innerWidth;
    h = canvas.height = window.innerHeight;
  }
  window.addEventListener('resize', resize);
  document.addEventListener('mousemove', function(e) {
    mouseX = e.clientX;
    mouseY = e.clientY;
  });
  resize();
  var time = 0;
  function draw() {
    time += 0.016;
    ctx.fillStyle = '#051828';
    ctx.fillRect(0, 0, w, h);
    for (var i = 0; i < layers.length; i++) {
      var L = layers[i];
      var baseAmp = L.amp;
      var ripple = 0;
      if (mouseX >= 0 && mouseY >= 0) {
        var dx = (mouseX / w - 0.5) * 2;
        var dy = (mouseY / h - 0.5) * 2;
        var dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 0.8) ripple = (1 - dist / 0.8) * 35;
      }
      var amp = baseAmp + ripple;
      ctx.beginPath();
      ctx.moveTo(0, h + 50);
      ctx.lineTo(0, h * L.yOffset);
      for (var x = 0; x <= w + 10; x += 10) {
        var t = (x / w) * 4 * Math.PI + time * (1 + i * 0.2);
        var y = h * L.yOffset + Math.sin(t) * amp + Math.sin(t * 0.7 + i) * amp * 0.3;
        ctx.lineTo(x, y);
      }
      ctx.lineTo(w + 10, h + 50);
      ctx.closePath();
      ctx.fillStyle = L.color;
      ctx.fill();
    }
    requestAnimationFrame(draw);
  }
  draw();
})();
