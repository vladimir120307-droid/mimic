import SwiftUI

@main
struct MimicApp: App {
    var body: some Scene {
        WindowGroup {
            NavigationStack {
                SettingsView()
            }
        }
    }
}
