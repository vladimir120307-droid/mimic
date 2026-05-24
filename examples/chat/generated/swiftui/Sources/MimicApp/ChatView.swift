import SwiftUI

struct ChatView: View {
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 8) {
            VStack(alignment: .leading) {
                HStack {
                    Text("Anna").font(.headline)
                    Spacer()
                }
                    .padding()
                    .background(Color.mimicPrimary)
                    .foregroundColor(.white)
                VStack(alignment: .leading) {

                }
                    .padding()
                    .background(Color(hex: "#FFFFFF"))
                    .cornerRadius(12)
                    .shadow(radius: 2)
                VStack(alignment: .leading) {

                }
                    .padding()
                    .background(Color(hex: "#0EA5E9"))
                    .cornerRadius(12)
                    .shadow(radius: 2)
                VStack(alignment: .leading) {

                }
                    .padding()
                    .background(Color(hex: "#FFFFFF"))
                    .cornerRadius(12)
                    .shadow(radius: 2)
                TextField("Type a message", text: .constant(""))
                    .textFieldStyle(.roundedBorder)
                Button {} label: {
                    Image(systemName: "paperplane")
                }
                    .padding()
                    .background(Color.mimicPrimary)
                    .foregroundColor(.white)
                    .clipShape(Circle())
            }
            }
            .padding()
        }
        .background(Color.mimicBackground)
    }
}
