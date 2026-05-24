import SwiftUI

struct InboxView: View {
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 8) {
            VStack(alignment: .leading) {
                HStack {
                    Text("Messages").font(.headline)
                    Spacer()
                }
                    .padding()
                    .background(Color.mimicPrimary)
                    .foregroundColor(.white)
                TextField("Search conversations", text: .constant(""))
                    .textFieldStyle(.roundedBorder)
                VStack(alignment: .leading) {
                    NavigationLink(destination: ChatView()) {
                        HStack {
                            Text("Anna")
                            Spacer()
                            Image(systemName: "chevron.right").foregroundColor(.secondary)
                        }
                        .padding(.vertical, 8)
                    }
                    NavigationLink(destination: ChatView()) {
                        HStack {
                            Text("Boris")
                            Spacer()
                            Image(systemName: "chevron.right").foregroundColor(.secondary)
                        }
                        .padding(.vertical, 8)
                    }
                    NavigationLink(destination: ChatView()) {
                        HStack {
                            Text("Team")
                            Spacer()
                            Image(systemName: "chevron.right").foregroundColor(.secondary)
                        }
                        .padding(.vertical, 8)
                    }
                    HStack {
                        Text("Mike")
                        Spacer()
                    }
                        .padding(.vertical, 8)
                    HStack {
                        Text("Family")
                        Spacer()
                    }
                        .padding(.vertical, 8)
                }
            }
            }
            .padding()
        }
        .background(Color.mimicBackground)
    }
}
