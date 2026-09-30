/**
 * Motor City Hockey Staff Names Feed
 * Bound to Staff Master Contact Google Sheet.
 * Returns ONLY All Time Staff List columns A:B as categories + names.
 * No phone numbers or emails are exposed.
 */
const MCH_SHEET_ID = "1nIidt6yRihORBu5w-0tQv3fk8XAMFkgyytlRKg31wQ4";
const MCH_STAFF_TAB = "All Time Staff List";

function doGet(e) {
  const callback = (e && e.parameter && e.parameter.callback) || "";
  const sheet = SpreadsheetApp.openById(MCH_SHEET_ID).getSheetByName(MCH_STAFF_TAB);
  const values = sheet.getRange("A1:B200").getDisplayValues();
  const groups = [];
  let current = null;

  values.forEach(row => {
    const first = String(row[0] || "").trim();
    const second = String(row[1] || "").trim();
    if (!first && !second) return;

    if (first && !second) {
      current = { category: first, names: [] };
      groups.push(current);
      return;
    }

    if (first && second && current) {
      current.names.push((first + " " + second).replace(/\s+/g, " ").trim());
    }
  });

  const payload = JSON.stringify({
    updatedAt: new Date().toISOString(),
    groups: groups.filter(group => group.category && group.names.length)
  });

  const safeCallback = callback.replace(/[^\w.$]/g, "");
  const output = safeCallback ? safeCallback + "(" + payload + ");" : payload;

  return ContentService
    .createTextOutput(output)
    .setMimeType(safeCallback ? ContentService.MimeType.JAVASCRIPT : ContentService.MimeType.JSON);
}
