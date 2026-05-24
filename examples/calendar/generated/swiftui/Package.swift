// swift-tools-version:5.9
import PackageDescription

let package = Package(
    name: "MimicApp",
    platforms: [.iOS(.v16), .macOS(.v13)],
    products: [
        .executable(name: "MimicApp", targets: ["MimicApp"]),
    ],
    targets: [
        .executableTarget(name: "MimicApp", path: "Sources/MimicApp"),
    ]
)
