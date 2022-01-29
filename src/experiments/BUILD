package(default_visibility = ["//visibility:public"])

load("@rules_python//python:defs.bzl", "py_binary")
load("@main_py_deps//:requirements.bzl", "requirement")
load("@io_bazel_rules_kotlin//kotlin/internal/jvm:jvm.bzl", "kt_jvm_binary")

py_binary(
    name = "chat_server",
    srcs = ["chat_server.py"],
    deps = [
    "//proto:chat_py_proto",
    requirement("grpcio")
    ],
)

py_binary(
    name = "chat_client",
    srcs = ["chat_client.py"],
    deps = [
    "//proto:chat_py_proto",
    requirement("grpcio")
    ],
)

kt_jvm_binary(
    name = "journal_server",
    main_class = "org.st.journal.JournalServerKt",
    srcs = [
        "JournalServer.kt",
        "JournalService.kt",
     ],
     deps = [
         "//proto:journal_java_proto",
     ]
    )
