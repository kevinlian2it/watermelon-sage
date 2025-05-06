document.addEventListener('DOMContentLoaded', () => {
  const options    = Array.from(document.querySelectorAll('.watermelon-img'));
  const basket     = document.getElementById('basket');
  const scale    = document.getElementById('scale');
  const feedback   = document.getElementById('feedback');
  const fbText     = document.getElementById('feedback-text');
  const nextBtn    = document.getElementById('next-btn') || document.getElementById('results-btn');

  options.forEach(img => {
    const idx = img.id.split('-')[1];

    // play sound on click
    img.addEventListener('click', () => {
      const audio = document.getElementById(`audio-${idx}`);
      if (audio) audio.play();
    });

    // start dragging: set preview then hide original
    img.addEventListener('dragstart', e => {
      e.dataTransfer.setData('text/plain', idx);
      e.dataTransfer.setDragImage(img, img.width/2, img.height/2);
      // delay so browser grabs preview first
      setTimeout(() => img.classList.add('dragging'), 0);
    });

    // only restore if we never actually dropped
    img.addEventListener('dragend', () => {
      // if still draggable, user must have canceled—show it again
      if (img.getAttribute('draggable') === 'true') {
        img.classList.remove('dragging');
      }
    });
  });

  if (scale) {
    // allow dragging over the scale
    scale.addEventListener('dragover', e => e.preventDefault());
    scale.addEventListener('drop', e => {
  e.preventDefault();
  const picked = e.dataTransfer.getData('text/plain');

  // read the attribute directly:
  const newSrc = scale.getAttribute(`data-scale-${picked}`);
  if (newSrc) {
    scale.src = newSrc;
  } else {
    console.warn(`no data-scale-${picked} on`, scale);
  }
});
  }

  basket.addEventListener('dragover', e => e.preventDefault());
  basket.addEventListener('drop', e => {
  e.preventDefault();
  const picked = e.dataTransfer.getData('text/plain');
  const pickedImg = document.getElementById(`opt-${picked}`);

  // swap basket graphic & lock drags immediately
  basket.src = basket.src.replace('.png', '_full.png');
  options.forEach(o => o.setAttribute('draggable', 'false'));
  pickedImg.classList.add('dragging');
  // unlock Next/Results button
nextBtn.disabled = false;
nextBtn.classList.remove('disabled');
// when clicked, go to the saved URL
nextBtn.addEventListener('click', () => {
  window.location = nextBtn.dataset.nextUrl;
});

  // now POST to server to get updated score + correctness
  fetch(`/submit_answer/${window.CURRENT_SCENARIO}/${picked}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  })
  .then(res => res.json())
  .then(data => {
    // build “Correct!/Incorrect!” + explanation
    const isCorrect = data.correct;
    const label    = isCorrect ? 'Correct!' : 'Incorrect!';
    fbText.innerHTML = `<span class="${ isCorrect ? 'correct' : 'incorrect' }">${label}</span> ${pickedImg.dataset.feedback}`;
    feedback.classList.remove('hidden');

    // live‐update the score
    document.getElementById('score').textContent = data.score;
  })
  .catch(console.error);
});

});
