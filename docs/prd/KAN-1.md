# KAN-1 PRD

Drafted by the factory product peer. Human gate: `prd_review`. Not posted to Jira.

- Orchestrator session: `ses_2a27f5821d931001a26b64c7`
- Product session: `ses_1f5d3d51b40af61ff9cac058`
- Grounded in: `github.com/mckinleybmelton/roamly-ai` at `/agent/repos/roamly-ai`

## PRD

### Problem
Roamly AI’s repo and landing screen describe a different product than the one in `RoamlyAI/`. Contributors following the README get a hold-to-talk, fully offline Gemma/Core ML app, a conversation history UI, and an M4A recording pipeline. The running app is a tap-to-toggle continuous listener. Replies come from keyword templates in `GemmaModelManager`, or from Apple Foundation Models on iOS 26 when `SystemLanguageModel.default.isAvailable` is true. The landing status light still turns green and reads “Offline AI Ready” in the template path, because `loadLocalModel()` sets `isModelLoaded = true` even when `SentimentClassifier.mlmodelc` is missing (it is not in the bundle) and because `generationMode` stays `.templateFallback` until the first successful `generateResponse`. Speech uses `SFSpeechRecognizer` without `requiresOnDeviceRecognition`, while the README says voice recognition needs no network. `conversationHistory` is appended and then cleared in `startListening()`, and the UI renders only `lastResponse`. `AudioRecorderViewModel` writes `.m4a` files that nothing plays or transcribes. Root `Package.swift` depends on `ai-edge-swift` / `AIEdge` and is not part of the Xcode app. `Info.plist` `UIBackgroundModes` includes `background-processing` and `background-audio`, which are not valid mode strings, plus a non-key `AVAudioSessionCategoryPlayAndRecord`.

### Users
- Travelers using the iOS prototype, who decide whether to trust the status light, speak, and grant the microphone, speech, and location permissions.
- Developers and reviewers of github.com/mckinleybmelton/roamly-ai who set up the Xcode project, judge privacy claims, and try to build the app.

### Scope
Epic KAN-1 is done when KAN-4 through KAN-10 are done and the RoamlyAI target builds cleanly for the iOS Simulator. Ship the README last so it describes the app after the other children land. Suggested order: KAN-8, KAN-6, KAN-7, KAN-5, KAN-10, KAN-9, KAN-4.

**KAN-4 — Rewrite the README (S, High).** Replace `README.md` so it matches the Xcode app at `RoamlyAI/RoamlyAI.xcodeproj` (target RoamlyAI, bundle id `com.roamly.RoamlyAI`, deployment target iOS 15.0, Swift 5, iPhone and iPad). Document what the code does today, as updated by the other children:

- Entry is `LandingView`: tap the mic to start or stop continuous listening, with live transcription, a paused state on audio-session interruptions, and a separate location status line.
- Replies are keyword/template travel answers (weather, food, stay, sights, transport, budget, safety, culture, plus location-phrased questions) from `GemmaModelManager`. On iOS 26, when Foundation Models are available, `FoundationModelBridge` can answer with on-device generation grounded by cached Wikipedia `GeoFact`s.
- The map-pin sheet is `DestinationSetupView`: search a city, download English Wikipedia geo extracts through `WikipediaFactsService`, cache them in `GeoFactsStore`, and delete a city. That download needs a network. Nearby place names come from MapKit local search.
- Permissions already in `Info.plist`: microphone, speech recognition, and location when in use.
- Point setup at `RoamlyAI/RoamlyAI.xcodeproj`. The workspace only wraps that project. No shared `.xcscheme` is checked in.
- State the speech behavior chosen in KAN-10, the status labels chosen in KAN-5, and that conversation turns are visible (KAN-9).
- Drop claims the tree does not support: hold-to-talk, a bundled Gemma or Core ML model, “no internet required” for the whole app, an M4A recording feature, a displayed history that is also an unchecked future item, `TravelAIService` as an API placeholder, and a `LICENSE` file (none is in the repo).

**KAN-5 — Honest engine status (S, High).** The landing model indicator (dot plus `modelStatusText`, including the footer that repeats it) reflects the engine before the first question:

- On-device generative path available (`FoundationModelBridge.isAvailable`): the existing “On-Device AI Ready” treatment (green).
- Template/keyword path: a different label and a non-green dot. The label “Offline AI Ready” is retired for this path.
- Load in progress: the existing loading treatment.
- Unavailable or failed: a non-ready treatment.
- A missing `SentimentClassifier.mlmodelc` does not count as a loaded model. `loadLocalModel()`’s catch path today sets `isModelLoaded = true` and leaves `modelError` nil, which is why the light goes green on every launch.

The location status row stays as it is.

**KAN-6 — Remove the unused M4A recorder (S, Med).** Remove `AudioRecorderViewModel` from the app and from the Xcode target. `LandingView` keeps continuous listening through `SpeechRecognitionService` only. A listening session writes no `.m4a` under Documents. `AudioMessage` and `TravelQuery` in `AudioMessage.swift` have no other call sites; remove that file and its target membership with the recorder.

**KAN-7 — Fix invalid Info.plist background config (S, Med).** In `RoamlyAI/RoamlyAI/Info.plist`:

- Remove `background-processing` and `background-audio` from `UIBackgroundModes`.
- Remove the valid `audio` entry as well. The only background-oriented recording path is `AudioRecorderViewModel`’s continuous M4A session, which KAN-6 removes. The app has no `BGTaskScheduler` use, so do not rename `background-processing` to `processing` and do not add `BGTaskSchedulerPermittedIdentifiers`.
- Remove the unrecognized key `AVAudioSessionCategoryPlayAndRecord`.
- Leave the microphone, speech-recognition, and location usage strings in place.

**KAN-8 — Delete the unused package and Gemma package stub (S, Med).** Delete root `Package.swift`. It declares an SPM library that depends on `https://github.com/google-ai-edge/ai-edge-swift.git` product `AIEdge`, and the repo has no `Sources/` tree for that target. The Xcode project does not link it. Keep `GemmaModelManager.swift` and `FoundationModelBridge.swift`. They are the live reply engine (`TravelAIService` calls them on every query). There is no second Gemma source file, weight, or model resource to delete.

**KAN-9 — Show conversation history (S, Low).** The landing screen shows turns already stored as `ConversationItem` (user query and reply). After two completed answers in one launch, both turns are on screen in chronological order, in a scrollable area. Stopping and starting listening in the same launch keeps those turns (`startListening()` currently calls `conversationHistory.removeAll()`). Saving history across relaunch is not required.

**KAN-10 — On-device speech, or an honest disclosure (S, Low).** Either outcome passes:

- Force on-device recognition (`requiresOnDeviceRecognition` on the recognition request). When on-device recognition is unavailable, the landing screen says so and the app does not send that audio to Apple’s speech servers.
- Or keep server-eligible recognition, and say so on the landing screen and in the README: speech may be processed by Apple’s speech service, and a network may be required. Locale remains `en-US` unless a later ticket adds languages.

**Simulator build (epic done-when).** This PRD was written on Linux. No iOS Simulator build was run here, and this environment cannot run one. A clean build means: on a Mac, Xcode builds the **RoamlyAI** target in `RoamlyAI/RoamlyAI.xcodeproj` for a generic iOS Simulator destination with no compile errors. Verify that on the macOS CI from KAN-11, or on a Mac worker. There is no checked-in shared scheme; build the RoamlyAI target directly.

### Out of scope
- Posting this PRD to Jira, changing labels, or approving the PRD gate.
- A new visual design, text-to-speech, bookings, maps UI, or extra languages.
- Rewriting template copy or Foundation Model instructions.
- Shipping a Gemma, Core ML, or AIEdge model, or renaming `GemmaModelManager` in this epic.
- Persisting conversation history to disk, or adding an account.
- Background listening or background processing as a feature.
- Adding a `LICENSE` file. The README simply stops citing one.
- Changing the iOS 15 deployment target, bundle id, or Wikipedia download behavior.
- Treating the location status light as a bug.

### Acceptance criteria
- KAN-4: A reader of `README.md` can name the real flow (tap to start/stop continuous listening), the two reply paths (templates, and Foundation Models on iOS 26 when available), destination Wikipedia download and its network need, location when-in-use, and the actual source files. The README does not tell them to hold the mic, load a Gemma/Core ML model, open a `LICENSE` file, or configure M4A recording.
- KAN-4: README speech wording matches the KAN-10 choice, and README status wording matches the KAN-5 labels.
- KAN-5: With Foundation Models available, the model status shows the on-device ready state before any question is asked.
- KAN-5: With Foundation Models unavailable, including a build that has no `SentimentClassifier.mlmodelc`, the model status does not show a green dot and does not read “Offline AI Ready”. Loading and failure look different from either ready state.
- KAN-6: Starting and stopping listening creates no `.m4a` file. `AudioRecorderViewModel.swift` and `AudioMessage.swift` are out of the Xcode target. The mic button still starts and stops `SpeechRecognitionService`.
- KAN-7: `UIBackgroundModes` is absent or empty. It does not contain `audio`, `background-audio`, `background-processing`, or `processing`. `AVAudioSessionCategoryPlayAndRecord` is gone. The three usage-description strings remain.
- KAN-8: Root `Package.swift` is gone. `GemmaModelManager.swift` and `FoundationModelBridge.swift` remain in the RoamlyAI target. The app target does not depend on `ai-edge-swift`.
- KAN-9: In one launch, two completed questions show both queries and both replies in time order. Stop then start listening again and those turns are still visible. Force-quit is allowed to clear them.
- KAN-10: Either recognition requests require on-device recognition and the UI explains when that is unavailable, or the landing screen and README both state that speech may be sent to Apple’s servers.
- Epic build: A Mac build of target RoamlyAI from `RoamlyAI/RoamlyAI.xcodeproj` for iOS Simulator finishes with no compile errors, via KAN-11 macOS CI or a Mac worker. A Linux checkout is not evidence of that build.

### Open questions
- Final words for the template-path status label (meaning is fixed: basic/template replies, distinct from “On-Device AI Ready”). Design can pick the string.
- KAN-10 still allows either on-device-only speech or a server disclosure. Privacy-sensitive travelers are the reason to prefer on-device-only if the supported-device check is straightforward; disclosure is an acceptable ship if on-device recognition is too narrow for the prototype.
- Whether the README should keep a “microphone needs a physical device” caveat. The epic build bar is a clean Simulator compile, not a Simulator mic test.
- KAN-11’s exact job name was not read for this draft. The verification owner is that macOS CI or a Mac worker.
- Whether any future ticket should restore background listening. This epic removes the background mode instead of correcting it into a real background feature.
