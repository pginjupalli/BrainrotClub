import React from "react";
import TextField from "@mui/material/TextField";
import theme from "../../theme"
import { Divider, Typography } from "@mui/material";

export default function page() {
  return (
    <>
      <Typography variant="h1" align="center" gutterBottom>
        Create Post
      </Typography>
      <Divider/>
      <TextField
        required
        id="filled-required"
        label="Event Name"
        variant="standard"
      />
    </>
  );
}
