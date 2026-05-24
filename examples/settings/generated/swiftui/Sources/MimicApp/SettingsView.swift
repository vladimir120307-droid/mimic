import SwiftUI

struct SettingsView: View {
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 8) {
            VStack(alignment: .leading) {
                HStack {
                    Text("Settings").font(.headline)
                    Spacer()
                }
                    .padding()
                    .background(Color.mimicPrimary)
                    .foregroundColor(.white)
                VStack(alignment: .leading) {
                    Text("Vladimir").font(.system(size: 18.0)).fontWeight(.bold)
                    Text("vladimir@example.com").font(.system(size: 13.0)).foregroundColor(Color(hex: "#64748B"))
                }
                    .padding()
                    .background(Color(hex: "#FFFFFF"))
                    .cornerRadius(12)
                    .shadow(radius: 2)
                VStack(alignment: .leading) {
                    HStack {
                        Text("Push notifications").font(.system(size: 15.0))
                        Toggle("", isOn: .constant(true)).labelsHidden()
                    }
                    HStack {
                        Text("Email digest").font(.system(size: 15.0))
                        Toggle("", isOn: .constant(true)).labelsHidden()
                    }
                    HStack {
                        Text("Do not disturb").font(.system(size: 15.0))
                        Toggle("", isOn: .constant(true)).labelsHidden()
                    }
                }
                    .padding()
                    .background(Color(hex: "#FFFFFF"))
                    .cornerRadius(12)
                    .shadow(radius: 2)
                Button("Sign out") {}
                    .buttonStyle(.borderedProminent)
            }
            }
            .padding()
        }
        .background(Color.mimicBackground)
    }
}
