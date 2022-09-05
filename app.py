#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for full license information.
"""
Speech synthesis samples for the Microsoft Cognitive Services Speech SDK
"""

try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:
    print("""
    Importing the Speech SDK for Python failed.
    Refer to
    https://docs.microsoft.com/azure/cognitive-services/speech-service/quickstart-text-to-speech-python for
    installation instructions.
    """)
    import sys
    sys.exit(1)


# Set up the subscription info for the Speech Service:
# Replace with your own subscription key and service region (e.g., "westus").
speech_key, service_region = "454890a85395450db9177023b54497cd", "eastus"

def test():

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name='en-US-JennyNeural'

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # Get text from the console and synthesize to the default speaker.
    print("Enter some text that you want to speak >")
    text = input()

    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

test()
def speech_synthesis_viseme_event():
    """performs speech synthesis and shows the viseme event."""
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Creates a speech synthesizer with a null output stream.
    # This means the audio output data will not be written to any output channel.
    # You can just get the audio from the result.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    # Subscribes to viseme received event
    # The unit of evt.audio_offset is tick (1 tick = 100 nanoseconds), divide it by 10,000 to convert to milliseconds.
    speech_synthesizer.viseme_received.connect(lambda evt: print("Viseme event received: audio offset: {}ms, viseme id: {}.".format(evt.audio_offset / 10000, evt.viseme_id)))

    # Receives a text from console input and synthesizes it to result.
    while True:
        print("Enter some text that you want to synthesize, Ctrl-Z to exit")
        try:
            text = input()
        except EOFError:
            break
        result = speech_synthesizer.speak_text_async(text).get()
        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(text))
            audio_data = result.audio_data
            print("{} bytes of audio data received.".format(len(audio_data)))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))


def speech_synthesis_bookmark_event():
    """performs speech synthesis and shows the bookmark event."""
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Creates a speech synthesizer with a null output stream.
    # This means the audio output data will not be written to any output channel.
    # You can just get the audio from the result.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    # Subscribes to viseme received event
    # The unit of evt.audio_offset is tick (1 tick = 100 nanoseconds), divide it by 10,000 to convert to milliseconds.
    speech_synthesizer.bookmark_reached.connect(lambda evt: print(
        "Bookmark reached: {}, audio offset: {}ms, bookmark text: {}.".format(evt, evt.audio_offset / 10000, evt.text)))

    print("Press Enter to start synthesizing.")
    input()

    # Bookmark tag is needed in the SSML, e.g.
    ssml = "<speak version='1.0' xml:lang='en-US' xmlns='http://www.w3.org/2001/10/synthesis' " \
           "xmlns:mstts='http://www.w3.org/2001/mstts'>" \
           "<voice name='Microsoft Server Speech Text to Speech Voice (en-US, AriaNeural)'>" \
           "<bookmark mark='bookmark_one'/> one. " \
           "<bookmark mark='bookmark_two'/> two. three. four.</voice></speak> "

    result = speech_synthesizer.speak_ssml_async(ssml).get()
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))


def speech_synthesis_with_auto_language_detection_to_speaker():
    """performs speech synthesis to the default speaker with auto language detection
       Note: this is a preview feature, which might be updated in future versions."""
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # create the auto-detection language configuration without specific languages
    auto_detect_source_language_config = \
        speechsdk.languageconfig.AutoDetectSourceLanguageConfig()

    # Creates a speech synthesizer using the default speaker as audio output.
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, auto_detect_source_language_config=auto_detect_source_language_config)

    while True:
        # Receives a text from console input and synthesizes it to speaker.
        # For example, you can input "Bonjour le monde. Hello world.", then you will hear "Bonjour le monde."
        # spoken in a French voice and "Hello world." in an English voice.
        print("Enter some multi lingual text that you want to speak, Ctrl-Z to exit")
        try:
            text = input()
        except EOFError:
            break
        result = speech_synthesizer.speak_text_async(text).get()
        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized to speaker for text [{}]".format(text))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))


def speech_synthesis_get_available_voices():
    """gets the available voices list."""

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Creates a speech synthesizer.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    print("Enter a locale in BCP-47 format (e.g. en-US) that you want to get the voices of, "
          "or enter empty to get voices in all locales.")
    try:
        text = input()
    except EOFError:
        pass

    result = speech_synthesizer.get_voices_async(text).get()
    # Check result
    if result.reason == speechsdk.ResultReason.VoicesListRetrieved:
        print('Voices successfully retrieved, they are:')
        for voice in result.voices:
            print(voice.name)
    elif result.reason == speechsdk.ResultReason.Canceled:
        print("Speech synthesis canceled; error details: {}".format(result.error_details))

if __