import SwiftUI

struct LoginView: View {
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 8) {
            VStack(alignment: .leading) {
                Image(systemName: "bolt")
                Text("Welcome back").font(.system(size: 28.0)).fontWeight(.bold)
                Text("Sign in to continue to your dashboard").font(.system(size: 14.0)).foregroundColor(Color(hex: "#64748B"))
                TextField("Email address", text: .constant(""))
                    .textFieldStyle(.roundedBorder)
                TextField("Password", text: .constant(""))
                    .textFieldStyle(.roundedBorder)
                Button("Sign in") {}
                    .buttonStyle(.borderedProminent)
                Text("Don't have an account? Create one").font(.system(size: 13.0)).foregroundColor(Color(hex: "#6E56CF"))
            }
            }
            .padding()
        }
        .background(Color.mimicBackground)
    }
}
