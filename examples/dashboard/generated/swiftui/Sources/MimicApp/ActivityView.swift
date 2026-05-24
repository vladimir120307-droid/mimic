import SwiftUI

struct ActivityView: View {
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 8) {
            VStack(alignment: .leading) {
                HStack {
                    Text("Recent activity").font(.headline)
                    Spacer()
                }
                    .padding()
                    .background(Color.mimicPrimary)
                    .foregroundColor(.white)
                Text("No activity yet — start recording to see something here").font(.system(size: 15.0)).foregroundColor(Color(hex: "#94A3B8"))
            }
            }
            .padding()
        }
        .background(Color.mimicBackground)
    }
}
