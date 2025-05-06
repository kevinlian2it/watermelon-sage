document.addEventListener('DOMContentLoaded', () => {
  const pairs = [
    { imgId: 'good-img', audioId: 'good-audio' },
    { imgId: 'bad-img',  audioId: 'bad-audio'  }
  ];

  pairs.forEach(({ imgId, audioId }) => {
    const img   = document.getElementById(imgId);
    const audio = document.getElementById(audioId);
    
    // only if both img and audio exist
    if (img && audio) {
      img.addEventListener('click', () => {
        audio.currentTime = 0;
        audio.play().catch(err => console.error('Audio play failed:', err));
      });
    }
  });
});
