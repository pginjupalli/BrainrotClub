"use client";

import React from "react";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import * as yup from "yup";
import {
  Typography,
  Divider,
  Grid,
  TextField,
  Button,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
  FormHelperText,
  Box,
  CircularProgress,
} from "@mui/material";
import { styled } from "@mui/material/styles";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";

import { createTheme, ThemeProvider } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    mode: "light", // Change this to "light" if it's currently "dark"
  },
});



/* 
  1. Define your form data interface.
     We include "referenceImages" as a FileList or null
     because you have an upload field in your design.
*/
interface FormData {
  eventName: string;
  audience: string;
  clubName: string;
  description: string;
  tone: string;
  primaryColor: string;
  secondaryColor: string;
  referenceImages: FileList | null;
}

/*
  2. Set up a Yup validation schema for the inputs.
     Adjust required fields and messages as needed.
*/
const formSchema = yup.object().shape({
  eventName: yup.string().required("Event name is required"),
  audience: yup.string().required("Audience is required"),
  clubName: yup.string().required("Club name is required"),
  description: yup.string().required("Event description is required"),
  tone: yup.string().required("Tone selection is required"),
  primaryColor: yup.string().required("Primary color is required"),
  secondaryColor: yup.string().required("Secondary color is required"),
  // referenceImages is more complicated to validate in Yup because it's a FileList,
  // but you could do something like this if necessary:
  // referenceImages: yup
  //   .mixed()
  //   .test("fileSize", "Files are too large", (value) => {
  //     // custom logic
  //   }),
});

/*
  3. A visually hidden input for file uploads 
     that will be triggered by clicking the "Upload Reference Images" button.
*/
const VisuallyHiddenInput = styled("input")({
  clip: "rect(0 0 0 0)",
  clipPath: "inset(50%)",
  height: 1,
  overflow: "hidden",
  position: "absolute",
  bottom: 0,
  left: 0,
  whiteSpace: "nowrap",
  width: 1,
});

export default function CreatePostPage() {
  // For user feedback (loading state, error display, etc.)
  const [isSubmitting, setIsSubmitting] = React.useState(false);
  const [submitError, setSubmitError] = React.useState<string | null>(null);

  /*
    4. Initialize react-hook-form with default values & validation schema.
       If you'd like default values for certain fields, set them here.
  */
  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
  } = useForm<FormData>({
    resolver: yupResolver(formSchema),
    defaultValues: {
      eventName: "",
      audience: "",
      clubName: "",
      description: "",
      tone: "",
      primaryColor: "",
      secondaryColor: "",
      referenceImages: null,
    },
  });

  /*
    5. Handle file changes for "referenceImages."
       We manually call setValue(...) from react-hook-form.
  */
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setValue("referenceImages", e.target.files, { shouldValidate: true });
    }
  };

  /*
    6. Simulated submission function. In a real app, you'd call an API or server here.
       Replace this with your actual submission logic (fetch/axios, etc.).
  */
  const mockSubmit = (data: FormData) =>
    new Promise<void>((resolve, reject) => {
      // Just simulating a network call
      setTimeout(() => {
        // 50% chance of success/failure
        Math.random() > 0.5 ? resolve() : reject(new Error("Random failure"));
      }, 1500);
    });

  /*
    7. handleSubmit logic that calls your submission function,
       sets error messages, and manages loading state.
  */
  const onSubmit = async (data: FormData) => {
    try {
      setIsSubmitting(true);
      setSubmitError(null);
      await mockSubmit(data);
      alert("Post created successfully!");
      // Optionally reset the form or do something else
      // e.g. reset();
    } catch (err) {
      setSubmitError((err as Error).message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Box
      component="form"
      onSubmit={handleSubmit(onSubmit)}
      sx={{ maxWidth: 900, mx: "auto", p: 2 }}
    >
      {/* Page Title */}
      <Typography variant="h2" align="center" gutterBottom>
        Create Post
      </Typography>
      <Divider sx={{ mb: 3 }} />

      {/* EVENT OVERVIEW */}
      <Typography variant="h5" gutterBottom>
        Event Overview
      </Typography>
      <Divider sx={{ mb: 2 }} />

      <Grid container spacing={2}>
        <Grid item xs={12} sm={4}>
          <TextField
            label="Event Name"
            variant="standard"
            fullWidth
            error={Boolean(errors.eventName)}
            helperText={errors.eventName?.message}
            // "register" is how we connect RHF to the TextField
            {...register("eventName")}
          />
        </Grid>
        <Grid item xs={12} sm={4}>
          <TextField
            label="Audience"
            variant="standard"
            fullWidth
            error={Boolean(errors.audience)}
            helperText={errors.audience?.message}
            {...register("audience")}
          />
        </Grid>
        <Grid item xs={12} sm={4}>
          <TextField
            label="Club Name"
            variant="standard"
            fullWidth
            error={Boolean(errors.clubName)}
            helperText={errors.clubName?.message}
            {...register("clubName")}
          />
        </Grid>
      </Grid>

      {/* ADDITIONAL DETAILS */}
      <Typography variant="h5" sx={{ mt: 4 }} gutterBottom>
        Additional Details
      </Typography>
      <Divider sx={{ mb: 2 }} />

      <TextField
        label="Event Description"
        multiline
        rows={4}
        variant="standard"
        fullWidth
        error={Boolean(errors.description)}
        helperText={errors.description?.message}
        {...register("description")}
      />

      {/* CUSTOMIZATION */}
      <Typography variant="h5" sx={{ mt: 4 }} gutterBottom>
        Customization
      </Typography>
      <Divider sx={{ mb: 2 }} />

      <Grid container spacing={2} alignItems="center">
        <Grid item xs={12} sm={3}>
          <FormControl
            variant="standard"
            fullWidth
            error={Boolean(errors.tone)}
          >
            <InputLabel id="tone-label">Tone</InputLabel>
            <Select
              labelId="tone-label"
              label="Tone"
              {...register("tone")}
              defaultValue="" // needed so MUI can track the default properly
            >
              <MenuItem value="">Select a tone</MenuItem>
              <MenuItem value="Excited">Excited</MenuItem>
              <MenuItem value="Friendly">Friendly</MenuItem>
              <MenuItem value="Professional">Professional</MenuItem>
              <MenuItem value="Monotone">Monotone</MenuItem>
              <MenuItem value="Angry">Angry</MenuItem>
            </Select>
            {errors.tone && <FormHelperText>{errors.tone.message}</FormHelperText>}
          </FormControl>
        </Grid>

        <Grid item xs={12} sm={3}>
          <TextField
            label="Primary Color"
            variant="standard"
            fullWidth
            error={Boolean(errors.primaryColor)}
            helperText={errors.primaryColor?.message}
            {...register("primaryColor")}
          />
        </Grid>
        <Grid item xs={12} sm={3}>
          <TextField
            label="Secondary Color"
            variant="standard"
            fullWidth
            error={Boolean(errors.secondaryColor)}
            helperText={errors.secondaryColor?.message}
            {...register("secondaryColor")}
          />
        </Grid>

        <Grid item xs={12} sm={3}>
          <Button
            component="label"
            variant="outlined"
            startIcon={<CloudUploadIcon />}
            sx={{ mt: 1 }}
          >
            Upload Reference Images
            <VisuallyHiddenInput
              type="file"
              multiple
              accept="image/*"
              onChange={handleFileChange}
            />
          </Button>
        </Grid>
      </Grid>

      {/* Error message if submission fails */}
      {submitError && (
        <Typography color="error" sx={{ mt: 2 }}>
          {submitError}
        </Typography>
      )}

      {/* Create/Submit button. We show a loader if isSubmitting is true. */}
      <Box sx={{ display: "flex", justifyContent: "flex-end", mt: 5 }}>
        <Button
          type="submit"
          variant="contained"
          size="large"
          disabled={isSubmitting}
        >
          {isSubmitting ? <CircularProgress size={24} /> : "Create"}
        </Button>
      </Box>
    </Box>
  );
}
