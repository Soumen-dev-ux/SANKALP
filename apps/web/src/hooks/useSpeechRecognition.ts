import { useEffect, useRef, useState } from "react";

import type {
  SpeechRecognitionInstance,
} from "../types/speech";

export function useSpeechRecognition(
  onTranscript: (text: string) => void
) {

  const recognitionRef =
    useRef<SpeechRecognitionInstance | null>(
      null
    );

  const [isListening, setIsListening] =
    useState(false);

  const [supported] =
    useState(() =>
      typeof window !== "undefined" &&
      Boolean(
        window.SpeechRecognition ||
        window.webkitSpeechRecognition
      )
    );

  const [error, setError] =
    useState<string | null>(null);

  useEffect(() => {

    const SpeechRecognition =
      window.SpeechRecognition ||
      window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      return;
    }

    const recognition =
      new SpeechRecognition();

    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = "en-IN";

    recognition.onstart = () => {

      setIsListening(true);
      setError(null);

    };

    recognition.onend = () => {

      setIsListening(false);

    };

    recognition.onresult = (event) => {

      let transcript = "";

      for (
        let i = 0;
        i < event.results.length;
        i++
      ) {

        transcript +=
          event.results[i][0].transcript;
      }

      onTranscript(
        transcript.trim()
      );
    };

    recognition.onerror = (event) => {
      console.error(
        "Speech recognition error:",
        event.error
      );

      setIsListening(false);

      let userFriendlyMessage = event.error;

      if (event.error === "network") {
        userFriendlyMessage =
          "Browser speech service is unreachable (Google Cloud Speech server blocked by browser privacy/network settings). You can type your request directly.";
      } else if (
        event.error === "not-allowed" ||
        event.error === "service-not-allowed"
      ) {
        userFriendlyMessage =
          "Microphone permission denied. Please allow microphone access in your browser settings.";
      } else if (event.error === "no-speech") {
        userFriendlyMessage =
          "No speech detected. Please speak clearly into your microphone.";
      } else if (event.error === "audio-capture") {
        userFriendlyMessage =
          "No microphone detected. Please check your audio input device.";
      }

      setError(userFriendlyMessage);
    };

    recognitionRef.current =
      recognition;

    return () => {
      try {
        recognition.abort();
      } catch (err) {
        console.error("Failed to abort speech recognition:", err);
      }
    };

  }, [onTranscript]);

  const startListening = async (
    language = "en-IN"
  ) => {

    if (!recognitionRef.current) {
      return;
    }

    setError(null);

    try {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        await navigator.mediaDevices.getUserMedia({ audio: true });
      }
    } catch (err) {
      console.warn("Microphone permission check warning:", err);
    }

    try {
      recognitionRef.current.lang =
        language;

      recognitionRef.current.start();
    } catch (err) {
      console.error("Failed to start speech recognition:", err);
      setError("Unable to start voice input. Please try again.");
    }

  };

  const stopListening = () => {
    try {
      recognitionRef.current?.stop();
    } catch (err) {
      console.error("Failed to stop speech recognition:", err);
    }
  };

  return {
    supported,
    isListening,
    error,
    startListening,
    stopListening,
  };
}