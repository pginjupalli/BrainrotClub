"use client";

import * as React from "react";
import Box from "@mui/material/Box";
import CssBaseline from "@mui/material/CssBaseline";
import Divider from "@mui/material/Divider";
import Drawer from "@mui/material/Drawer";
import AddCircleOutlineIcon from "@mui/icons-material/AddCircleOutline";
import DraftsIcon from "@mui/icons-material/Drafts";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import MovieIcon from "@mui/icons-material/Movie";
import theme from "@/theme";

const drawerWidth = 240;

interface Props {
  /**
   * Injected by the documentation to work in an iframe.
   * Remove this when copying and pasting into your project.
   */
  window?: () => Window;
}

export default function ResponsiveDrawer(props: Props) {


  const icons = [
    <MovieIcon />,
    <AddCircleOutlineIcon />,
    <SmartToyIcon />,
    <DraftsIcon />,
  ];

  const drawer = (
    <div>
      <Typography
        variant="h6"
        p={2}
        bgcolor={theme.palette.primary.main}
        color="white"
      >
        CampusGenie
      </Typography>
      <Divider sx={{ bgcolor: "white" }} />
      <List>
        {["Create Post"].map((text, index) => (
          <ListItem key={text} disablePadding>
            <ListItemButton href="/createpost">
              <ListItemIcon sx={{ color: "white" }}>
                <AddCircleOutlineIcon />
              </ListItemIcon>
              <ListItemText primary={text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </div>
  );

  return (
    <div>
        <Drawer
          variant="persistent"
          sx={{
            display: { sm: "block" },
            "& .MuiDrawer-paper": {
              boxSizing: "border-box",
              width: drawerWidth,
              backgroundColor: theme.palette.primary.main,
              color: "white",
            },
          }}
          open
        >
          {drawer}
        </Drawer>
    </div>
  );
}
