#include "mimic/capture.h"
#include "mimic/dedup.h"

#include <pybind11/functional.h>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <cstring>

namespace py = pybind11;
using namespace mimic;

namespace {

py::array_t<uint8_t> frame_to_numpy(const Frame& frame) {
    const auto h = static_cast<py::ssize_t>(frame.height);
    const auto w = static_cast<py::ssize_t>(frame.width);
    py::array_t<uint8_t> arr({h, w, py::ssize_t{4}});
    auto* dst = static_cast<uint8_t*>(arr.mutable_data());
    if (frame.stride == frame.width * 4) {
        std::memcpy(dst, frame.data.data(), frame.data.size());
    } else {
        for (int y = 0; y < frame.height; ++y) {
            std::memcpy(dst + static_cast<size_t>(y) * frame.width * 4,
                        frame.data.data() + static_cast<size_t>(y) * frame.stride,
                        static_cast<size_t>(frame.width) * 4);
        }
    }
    return arr;
}

}

PYBIND11_MODULE(_mimic_capture, m) {
    m.doc() = "Native screen-capture bindings for mimic";

    m.attr("__version__")     = version();
    m.attr("platform_name")   = platform_name();

    py::class_<Rect>(m, "Rect")
        .def(py::init<>())
        .def(py::init<int32_t, int32_t, int32_t, int32_t>(),
             py::arg("x"), py::arg("y"), py::arg("width"), py::arg("height"))
        .def_readwrite("x",      &Rect::x)
        .def_readwrite("y",      &Rect::y)
        .def_readwrite("width",  &Rect::width)
        .def_readwrite("height", &Rect::height);

    py::enum_<PixelFormat>(m, "PixelFormat")
        .value("BGRA8", PixelFormat::BGRA8)
        .value("RGBA8", PixelFormat::RGBA8);

    py::class_<Frame>(m, "Frame")
        .def_readonly("width",        &Frame::width)
        .def_readonly("height",       &Frame::height)
        .def_readonly("stride",       &Frame::stride)
        .def_readonly("format",       &Frame::format)
        .def_readonly("timestamp_ns", &Frame::timestamp_ns)
        .def_readonly("cursor_x",     &Frame::cursor_x)
        .def_readonly("cursor_y",     &Frame::cursor_y)
        .def_readonly("mouse_down",   &Frame::mouse_down)
        .def("as_numpy", &frame_to_numpy,
             "Return frame pixels as an (H, W, 4) uint8 numpy array.");

    py::class_<CaptureConfig>(m, "CaptureConfig")
        .def(py::init<>())
        .def_readwrite("region",          &CaptureConfig::region)
        .def_readwrite("target_fps",      &CaptureConfig::target_fps)
        .def_readwrite("include_cursor",  &CaptureConfig::include_cursor)
        .def_readwrite("enable_dedup",    &CaptureConfig::enable_dedup)
        .def_readwrite("dedup_threshold", &CaptureConfig::dedup_threshold)
        .def_readwrite("display_index",   &CaptureConfig::display_index);

    py::class_<DisplayInfo>(m, "DisplayInfo")
        .def_readonly("index",      &DisplayInfo::index)
        .def_readonly("name",       &DisplayInfo::name)
        .def_readonly("bounds",     &DisplayInfo::bounds)
        .def_readonly("dpi_scale",  &DisplayInfo::dpi_scale)
        .def_readonly("is_primary", &DisplayInfo::is_primary);

    py::class_<Capturer>(m, "Capturer")
        .def("start",      &Capturer::start)
        .def("stop",       &Capturer::stop)
        .def("is_running", &Capturer::is_running)
        .def("grab_one",   &Capturer::grab_one);

    m.def("make_capturer", &make_capturer);
    m.def("list_displays", &list_displays);

    py::class_<Deduplicator>(m, "Deduplicator")
        .def(py::init<float>(), py::arg("threshold") = 0.02f)
        .def("accept", &Deduplicator::accept)
        .def("reset",  &Deduplicator::reset);

    m.def("dhash",            &dhash, py::arg("frame"), py::arg("hash_size") = 8);
    m.def("hamming_distance", &hamming_distance);
}
