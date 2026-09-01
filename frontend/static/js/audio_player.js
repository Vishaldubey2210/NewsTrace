// Executive Audio Briefing Player Simulation using Web Speech Synthesis
function playAudioBrief(text) {
    if (!('speechSynthesis' in window)) {
        alert('Audio briefing speech synthesis not supported in this browser.');
        return;
    }
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    window.speechSynthesis.speak(utterance);
}
