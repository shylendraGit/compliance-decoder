import { Frame, Page } from "@shopify/polaris";
import { useAppBridge } from "@shopify/app-bridge-react";
import { useEffect, useState } from "react";

export default function HomePage() {
  const app = useAppBridge();
  const [shopOrigin, setShopOrigin] = useState("");

  useEffect(() => {
    const query = new URLSearchParams(window.location.search);
    setShopOrigin(query.get("shop") || "");
  }, []);

  const embeddedAppUrl = `https://hedgehog-chief-ram.ngrok-free.app?shop=${shopOrigin}`;

  return (
    <Frame>
      <Page title="RiskLens">
        <div style={{ height: "85vh" }}>
          <iframe
            src={embeddedAppUrl}
            style={{ width: "100%", height: "100%", border: "none" }}
            allowFullScreen
          ></iframe>
        </div>
      </Page>
    </Frame>
  );
}
