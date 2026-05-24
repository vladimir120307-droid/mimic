import SwiftUI

struct ProductView: View {
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 8) {
            VStack(alignment: .leading) {
                AsyncImage(url: URL(string: "https://picsum.photos/seed/linen/1200/800")) { phase in
                    phase.image?.resizable().aspectRatio(contentMode: .fill)
                }
                Text("Linen shirt").font(.system(size: 22.0)).fontWeight(.bold)
                Text("$48").font(.system(size: 18.0)).foregroundColor(Color(hex: "#E11D48"))
                Text("Soft, breathable linen with a relaxed cut. Ethically sourced.").font(.system(size: 14.0)).foregroundColor(Color(hex: "#64748B"))
                Button("Add to cart") {}
                    .buttonStyle(.borderedProminent)
            }
            }
            .padding()
        }
        .background(Color.mimicBackground)
    }
}
