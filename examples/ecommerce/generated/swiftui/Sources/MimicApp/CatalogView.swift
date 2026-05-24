import SwiftUI

struct CatalogView: View {
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 8) {
            VStack(alignment: .leading) {
                HStack {
                    Text("Shop").font(.headline)
                    Spacer()
                }
                    .padding()
                    .background(Color.mimicPrimary)
                    .foregroundColor(.white)
                TextField("Search products", text: .constant(""))
                    .textFieldStyle(.roundedBorder)
                ZStack {
                    VStack(alignment: .leading) {
                        AsyncImage(url: URL(string: "https://picsum.photos/seed/linen/400/400")) { phase in
                            phase.image?.resizable().aspectRatio(contentMode: .fill)
                        }
                        Text("Linen shirt").font(.system(size: 14.0)).fontWeight(.semibold)
                        Text("$48").font(.system(size: 15.0)).fontWeight(.bold).foregroundColor(Color(hex: "#E11D48"))
                    }
                        .padding()
                        .background(Color(hex: "#FFFFFF"))
                        .cornerRadius(12)
                        .shadow(radius: 2)
                    VStack(alignment: .leading) {
                        AsyncImage(url: URL(string: "https://picsum.photos/seed/sweater/400/400")) { phase in
                            phase.image?.resizable().aspectRatio(contentMode: .fill)
                        }
                        Text("Knit sweater").font(.system(size: 14.0)).fontWeight(.semibold)
                        Text("$72").font(.system(size: 15.0)).fontWeight(.bold).foregroundColor(Color(hex: "#E11D48"))
                    }
                        .padding()
                        .background(Color(hex: "#FFFFFF"))
                        .cornerRadius(12)
                        .shadow(radius: 2)
                    VStack(alignment: .leading) {
                        AsyncImage(url: URL(string: "https://picsum.photos/seed/coat/400/400")) { phase in
                            phase.image?.resizable().aspectRatio(contentMode: .fill)
                        }
                        Text("Wool coat").font(.system(size: 14.0)).fontWeight(.semibold)
                        Text("$195").font(.system(size: 15.0)).fontWeight(.bold).foregroundColor(Color(hex: "#E11D48"))
                    }
                        .padding()
                        .background(Color(hex: "#FFFFFF"))
                        .cornerRadius(12)
                        .shadow(radius: 2)
                    VStack(alignment: .leading) {
                        AsyncImage(url: URL(string: "https://picsum.photos/seed/trousers/400/400")) { phase in
                            phase.image?.resizable().aspectRatio(contentMode: .fill)
                        }
                        Text("Cotton trousers").font(.system(size: 14.0)).fontWeight(.semibold)
                        Text("$56").font(.system(size: 15.0)).fontWeight(.bold).foregroundColor(Color(hex: "#E11D48"))
                    }
                        .padding()
                        .background(Color(hex: "#FFFFFF"))
                        .cornerRadius(12)
                        .shadow(radius: 2)
                }
            }
            }
            .padding()
        }
        .background(Color.mimicBackground)
    }
}
