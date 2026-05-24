import SwiftUI

extension Color {
    static let mimicPrimary    = Color(hex: "#6E56CF")
    static let mimicBackground = Color(hex: "#F8FAFC")
    static let mimicSurface    = Color(hex: "#F8FAFC")
    static let mimicError      = Color(hex: "#E11D48")
    static let mimicOnSurface  = Color(hex: "#0F172A")

    init(hex: String) {
        let h = hex.trimmingCharacters(in: CharacterSet(charactersIn: "#"))
        var v: UInt64 = 0
        Scanner(string: h).scanHexInt64(&v)
        let r = Double((v >> 16) & 0xFF) / 255.0
        let g = Double((v >>  8) & 0xFF) / 255.0
        let b = Double( v        & 0xFF) / 255.0
        self = Color(red: r, green: g, blue: b)
    }
}
