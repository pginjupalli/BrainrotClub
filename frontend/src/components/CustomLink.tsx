import Link from "@mui/material/Link";
import NextLink from "next/link";

interface CustomLinkProps {
    href: string;
    newTab?: boolean;
    children: React.ReactNode;
}

const CustomLink = ({ href, newTab, children }: CustomLinkProps) => {
    return (
        <Link
            href={href}
            target={newTab ? "_blank" : ""}
            rel={newTab ? "noreferrer" : ""}
            component={NextLink}
            width="auto"
        >
            {children}
        </Link>
    );
};

export default CustomLink;
