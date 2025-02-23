"use client";
import { createTheme } from "@mui/material/styles";

const theme = createTheme({
    palette: {
        mode: "light", // Ensure it's in light mode
        primary: {
            main: "#6C63FF", // A soft violet-blue for a modern, fresh look
        },
        secondary: {
            main: "#FF6584", // A vibrant coral-pink for contrast
        },
        error: {
            main: "#D32F2F", // Standard Material UI error red
        },
        success: {
            main: "#4CAF50", // A fresh green for success messages
        },
        warning: {
            main: "#FFA726", // Orange for warnings
        },
        background: {
            default: "#F5F5F5", // A very light gray background
            paper: "#FFFFFF", // Pure white for cards and surfaces
        },
        text: {
            primary: "#222121",    // 15% darker thanrgb(22, 21, 21)
            secondary: "#222121",  // 13% darker than #555555
          },
    },
    typography: {
        fontFamily: "var(--font-roboto), sans-serif",
        h1: {
            fontWeight: 700,
            fontSize: "2.2rem",
        },
        h2: {
            fontWeight: 600,
            fontSize: "1.8rem",
        },
        h3: {
            fontWeight: 500,
            fontSize: "1.5rem",
        },
        button: {
            textTransform: "none", // Keeps button text lowercase for a sleek UI
            fontWeight: 600,
        },
    },
    shape: {
        borderRadius: 12, // Smooth rounded edges for UI components
    },
    components: {
        MuiButton: {
            styleOverrides: {
                root: {
                    borderRadius: 8, // Rounder buttons
                    padding: "8px 16px",
                },
            },
        },
        MuiPaper: {
            styleOverrides: {
                root: {
                    borderRadius: 12, // Smooth rounded card edges
                    padding: "16px",
                },
            },
        },
    },
});

export default theme;
