"use client";

import {
    AppBar,
    Button,
    Box,
    Toolbar,
    Typography,
    List,
    ListItem,
    ListItemButton,
    ListItemText,
    Drawer,
    IconButton,
    CssBaseline,
} from "@mui/material";

import MenuIconRounded from "@mui/icons-material/MenuRounded";
import CustomLink from "@/components/CustomLink";

import { useState } from "react";

import "./Navbar.css";

const NAME = "CampusGenie";

const NAV_ITEMS = [
    {
        title: "Test",
        href: "/test",
    },
];

const Navbar = () => {
    const [drawerOpen, setDrawerOpen] = useState(false);

    const handleDrawerToggle = () => {
        setDrawerOpen(!drawerOpen);
    };

    const drawer = (
        <Box
            id="nav-drawer"
            onClick={handleDrawerToggle}
            sx={{ textAlign: "center" }}
        >
            <List>
                {NAV_ITEMS.map((item) => (
                    <CustomLink key={item.title} href={item.href}>
                        <ListItem disablePadding>
                            <ListItemButton>
                                <ListItemText primary={item.title} />
                            </ListItemButton>
                        </ListItem>
                    </CustomLink>
                ))}
            </List>
        </Box>
    );

    return (
        <Box component="nav" id="navbar">
            <CssBaseline />
            <Box sx={{ display: "flex", justifyContent: "space-between" }}>
                <AppBar component="nav">
                    <Toolbar>
                        <CustomLink href="/">
                            <Typography variant="h6" color="">
                                {NAME}
                            </Typography>
                        </CustomLink>

                        <Box
                            sx={{
                                display: "flex",
                                flexGrow: 1,
                                justifyContent: "flex-end",
                            }}
                        >
                            <IconButton
                                color="inherit"
                                edge="start"
                                onClick={handleDrawerToggle}
                                sx={{
                                    display: { sm: "none" },
                                }}
                            >
                                <MenuIconRounded />
                            </IconButton>

                            <Box sx={{ display: { xs: "none", sm: "flex" } }}>
                                {NAV_ITEMS.map((item) => (
                                    <CustomLink
                                        key={item.title}
                                        href={item.href}
                                    >
                                        <Button sx={{ color: "#fff" }}>
                                            {item.title}
                                        </Button>
                                    </CustomLink>
                                ))}
                            </Box>
                        </Box>
                    </Toolbar>
                </AppBar>
            </Box>
            <nav>
                <Drawer
                    variant="temporary"
                    anchor="right"
                    open={drawerOpen}
                    onClose={handleDrawerToggle}
                    ModalProps={{
                        keepMounted: true,
                    }}
                    sx={{
                        display: { xs: "block", sm: "block" },
                        "& .MuiDrawer-paper": {
                            boxSizing: "border-box",
                            width: 240,
                        },
                    }}
                >
                    {drawer}
                </Drawer>
            </nav>
        </Box>
    );
};

export default Navbar;
