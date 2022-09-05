import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(subscription="454890a85395450db9177023b54497cd", region="eastus")
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

# The language of the voice that speaks.
speech_config.speech_synthesis_voice_name='en-US-JennyNeural'

# speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

# # Get text from the console and synthesize to the default speaker.
# print("Enter some text that you want to speak >")
# text = input()

# speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

# if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
#     print("Speech synthesized for text [{}]".format(text))
# elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
#     cancellation_details = speech_synthesis_result.cancellation_details
#     print("Speech synthesis canceled: {}".format(cancellation_details.reason))
#     if cancellation_details.reason == speechsdk.CancellationReason.Error:
#         if cancellation_details.error_details:
#             print("Error details: {}".format(cancellation_details.error_details))
#             print("Did you set the speech resource key and region values?")
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

def viseme_cb(evt):
    print("Viseme event received: audio offset: {}ms, viseme id: {}.".format(
        evt.audio_offset / 10000, evt.viseme_id))

    # `Animation` is an xml string for SVG or a json string for blend shapes
    animation = evt.animation

# Subscribes to viseme received event
speech_synthesizer.viseme_received.connect(viseme_cb)
ssml='''<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">
  <voice name="en-US-JennyNeural">
    <mstts:viseme type="FacialExpression"/>
    Rainbow has seven colors: Red, orange, yellow, green, blue, indigo, and violet.
  </voice>
</speak>'''
# If VisemeID is the only thing you want, you can also use `speak_text_async()`
result = speech_synthesizer.speak_ssml_async(ssml).get()