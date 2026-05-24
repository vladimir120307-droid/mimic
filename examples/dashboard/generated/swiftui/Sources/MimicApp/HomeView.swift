import SwiftUI

struct HomeView: View {
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 8) {
            VStack(alignment: .leading) {
                HStack {
                    Text("").font(.headline)
                    Spacer()
                }
                    .padding()
                    .background(Color.mimicPrimary)
                    .foregroundColor(.white)
                VStack(alignment: .leading) {
                    Text("Good morning, Vladimir").font(.system(size: 22.0)).fontWeight(.bold)
                }
                    .padding()
                    .background(Color(hex: "#EEF2FF"))
                    .cornerRadius(12)
                    .shadow(radius: 2)
                VStack(alignment: .leading) {
                    NavigationLink(destination: ActivityView()) {
                        HStack {
                            Text("Recent activity")
                            Spacer()
                            Image(systemName: "chevron.right").foregroundColor(.secondary)
                        }
                        .padding(.vertical, 8)
                    }
                    HStack {
                        Text("Saved projects")
                        Spacer()
                    }
                        .padding(.vertical, 8)
                    HStack {
                        Text("Settings")
                        Spacer()
                    }
                        .padding(.vertical, 8)
                }
                NavigationLink(destination: ActivityView()) {
                    Image(systemName: "plus")
                        .padding()
                        .background(Color.mimicPrimary)
                        .foregroundColor(.white)
                        .clipShape(Circle())
                }
            }
            }
            .padding()
        }
        .background(Color.mimicBackground)
    }
}
