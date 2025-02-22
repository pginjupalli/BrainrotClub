"use client";
import { createTheme } from "@mui/material/styles";

const theme = createTheme({
    palette: {
        type: "light",
        primary: {
            main: "#9e4a6f",
        },
        secondary: {
            main: "#0090f5",
        },
        error: {
            main: "#e20e11",
        },
    },
    typography: {
        fontFamily: "var(--font-roboto)",
    },
});

export default theme;
