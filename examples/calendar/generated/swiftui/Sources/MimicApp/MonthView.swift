import SwiftUI

struct MonthView: View {
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 8) {
            VStack(alignment: .leading) {
                HStack {
                    Text("May 2026").font(.headline)
                    Spacer()
                }
                    .padding()
                    .background(Color.mimicPrimary)
                    .foregroundColor(.white)
                HStack {
                    Text("Mon").font(.system(size: 12.0)).foregroundColor(Color(hex: "#64748B"))
                    Text("Tue").font(.system(size: 12.0)).foregroundColor(Color(hex: "#64748B"))
                    Text("Wed").font(.system(size: 12.0)).foregroundColor(Color(hex: "#64748B"))
                    Text("Thu").font(.system(size: 12.0)).foregroundColor(Color(hex: "#64748B"))
                    Text("Fri").font(.system(size: 12.0)).foregroundColor(Color(hex: "#64748B"))
                    Text("Sat").font(.system(size: 12.0)).foregroundColor(Color(hex: "#64748B"))
                    Text("Sun").font(.system(size: 12.0)).foregroundColor(Color(hex: "#64748B"))
                }
                VStack(alignment: .leading) {
                    HStack {
                        Text("1")
                        Spacer()
                    }
                        .padding(.vertical, 8)
                    HStack {
                        Text("2")
                        Spacer()
                    }
                        .padding(.vertical, 8)
                    HStack {
                        Text("3")
                        Spacer()
                    }
                        .padding(.vertical, 8)
                    HStack {
                        Text("4")
                        Spacer()
                    }
                        .padding(.vertical, 8)
                    HStack {
                        Text("5")
                        Spacer()
                    }
                        .padding(.vertical, 8)
                    HStack {
                        Text("6")
                        Spacer()
                    }
                        .padding(.vertical, 8)
                    HStack {
                        Text("7")
                        Spacer()
                    }
                        .padding(.vertical, 8)
                    HStack {
                        Text("8")
                        Spacer()
                    }
                        .padding(.vertical, 8)
                    HStack {
                        Text("9")
                        Spacer()
                    }
                        .padding(.vertical, 8)
                    HStack {
                        Text("10")
                        Spacer()
                    }
                        .padding(.vertical, 8)
                    HStack {
                        Text("11")
                        Spacer()
                    }
                        .padding(.vertical, 8)
                    HStack {
                        Text("12")
                        Spacer()
                    }
                        .padding(.vertical, 8)
                    HStack {
                        Text("13")
                        Spacer()
                    }
                        .padding(.vertical, 8)
                    HStack {
                        Text("14")
                        Spacer()
                    }
                        .padding(.vertical, 8)
                    HStack {
                        Text("15")
                        Spacer()
                    }
                        .padding(.vertical, 8)
                    HStack {
                        Text("16")
                        Spacer()
                    }
                        .padding(.vertical, 8)
                    HStack {
                        Text("17")
                        Spacer()
                    }
                        .padding(.vertical, 8)
                    HStack {
                        Text("18")
                        Spacer()
                    }
                        .padding(.vertical, 8)
                    HStack {
                        Text("19")
                        Spacer()
                    }
                        .padding(.vertical, 8)
                    HStack {
                        Text("20")
                        Spacer()
                    }
                        .padding(.vertical, 8)
                    HStack {
                        Text("21")
                        Spacer()
                    }
                        .padding(.vertical, 8)
                    HStack {
                        Text("22")
                        Spacer()
                    }
                        .padding(.vertical, 8)
                    HStack {
                        Text("23")
                        Spacer()
                    }
                        .padding(.vertical, 8)
                    HStack {
                        Text("24")
                        Spacer()
                    }
                        .padding(.vertical, 8)
                    HStack {
                        Text("25")
                        Spacer()
                    }
                        .padding(.vertical, 8)
                    HStack {
                        Text("26")
                        Spacer()
                    }
                        .padding(.vertical, 8)
                    HStack {
                        Text("27")
                        Spacer()
                    }
                        .padding(.vertical, 8)
                    HStack {
                        Text("28")
                        Spacer()
                    }
                        .padding(.vertical, 8)
                }
                VStack(alignment: .leading) {
                    Text("Next: Design review").font(.system(size: 16.0)).fontWeight(.bold)
                    Text("Tomorrow, 10:00").font(.system(size: 13.0)).foregroundColor(Color(hex: "#64748B"))
                }
                    .padding()
                    .background(Color(hex: "#ECFDF5"))
                    .cornerRadius(12)
                    .shadow(radius: 2)
            }
            }
            .padding()
        }
        .background(Color.mimicBackground)
    }
}
