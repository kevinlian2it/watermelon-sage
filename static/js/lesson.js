document.addEventListener('DOMContentLoaded', () => {
  const goodImg = document.getElementById('good-img');
  const badImg  = document.getElementById('bad-img');
  const goodAudio = document.getElementById('good-audio');
  const badAudio  = document.getElementById('bad-audio');

  // make cursor a pointer
  [goodImg, badImg].forEach(img => {
    img.style.cursor = 'pointer';
  });

  goodImg.addEventListener('click', () => {
    goodAudio.currentTime = 0;
    goodAudio.play();
  });

  badImg.addEventListener('click', () => {
    badAudio.currentTime = 0;
    badAudio.play();
  });
});
