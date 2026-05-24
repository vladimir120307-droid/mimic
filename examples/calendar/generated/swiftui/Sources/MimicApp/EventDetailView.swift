import SwiftUI

struct EventDetailView: View {
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 8) {
            VStack(alignment: .leading) {
                HStack {
                    Text("Design review").font(.headline)
                    Spacer()
                }
                    .padding()
                    .background(Color.mimicPrimary)
                    .foregroundColor(.white)
                Text("Friday May 22, 10:00 — 11:00").font(.system(size: 16.0))
                Text("Conference room B / Zoom").font(.system(size: 14.0)).foregroundColor(Color(hex: "#64748B"))
                Button("Join meeting") {}
                    .buttonStyle(.borderedProminent)
            }
            }
            .padding()
        }
        .background(Color.mimicBackground)
    }
}
