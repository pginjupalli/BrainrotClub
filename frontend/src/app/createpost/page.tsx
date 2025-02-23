"use client";

import React from "react";
import TextField from "@mui/material/TextField";
import theme from "../../theme";
import { Divider, Typography } from "@mui/material";
import Select, { SelectChangeEvent } from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import Button from "@mui/material/Button";
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { styled } from '@mui/material/styles';

export default function page() {
  const [tone, setTone] = React.useState("");

  const handleChange = (event: SelectChangeEvent) => {
    setTone(event.target.value);
  };

  const VisuallyHiddenInput = styled('input')({
    clip: 'rect(0 0 0 0)',
    clipPath: 'inset(50%)',
    height: 1,
    overflow: 'hidden',
    position: 'absolute',
    bottom: 0,
    left: 0,
    whiteSpace: 'nowrap',
    width: 1,
  });

  return (
    <>
      <Typography variant="h2" align="center" gutterBottom>
        Create Post
      </Typography>
      <Divider />
      <Typography variant="h5" pt={5}>
        Event Overview
      </Typography>
      <Divider color="black" />
      <div style={{ marginTop: 10 }}>
        <TextField
          required
          id="filled-required"
          label="Event Name"
          variant="standard"
          style={{ marginRight: 60 }}
        />

        <TextField
          required
          id="filled-required"
          label="Audience"
          variant="standard"
          style={{ marginRight: 60 }}
        />

        <TextField
          required
          id="filled-required"
          label="Club Name"
          variant="standard"
          style={{ marginRight: 60 }}
        />
      </div>

      <Typography variant="h5" pt={5}>
        Additional Details
      </Typography>
      <Divider color="black" />

      <TextField
        id="standard-multiline-static"
        label="Event Description"
        multiline
        rows={4}
        variant="standard"
        style={{ marginTop: 10, width: "calc(94vw - 240px)" }}
      />

      <Typography variant="h5" pt={5}>
        Customization
      </Typography>
      <Divider color="black" />

      <div style={{ marginTop: 10 }}>
        <FormControl
          variant="standard"
          sx={{ minWidth: 120, marginRight: "60px" }}
        >
          <InputLabel id="demo-simple-select-standard-label">Tone</InputLabel>
          <Select
            labelId="demo-simple-select-standard-label"
            id="demo-simple-select-standard"
            value={tone}
            onChange={handleChange}
            label="Post Tone"
          >
            <MenuItem value="">None</MenuItem>
            <MenuItem value={"Excited"}>Excited</MenuItem>
            <MenuItem value={"Friendly"}>Polite</MenuItem>
            <MenuItem value={"Professional"}>Professional</MenuItem>
            <MenuItem value={"Monotone"}>Monotone</MenuItem>
            <MenuItem value={"Angry"}>Mean</MenuItem>
          </Select>
        </FormControl>

        <TextField
          id="filled-required"
          label="Primary Color"
          variant="standard"
          style={{ marginRight: 60 }}
        />

        <TextField
          id="filled-required"
          label="Secondary Color"
          variant="standard"
          style={{ marginRight: 60 }}
        />

        <Button
          component="label"
          role={undefined}
          variant="outlined"
          tabIndex={-1}
          startIcon={<CloudUploadIcon />}
          style={{ marginTop: 12 }}
        >
          Upload Reference Images
          <VisuallyHiddenInput
            type="file"
            onChange={(event) => console.log(event.target.files)}
            multiple
          />
        </Button>

        <Button
          variant="contained"
          size="large"
          sx={{ position: "fixed", bottom: 60, right: 70 }}
        >
          Create
        </Button>
      </div>
    </>
  );
}
