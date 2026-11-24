import { readFile } from 'node:fs/promises'
import AxeBuilder from '@axe-core/playwright'
import { expect, test } from '@playwright/test'

const isShowcase = process.env.THX_SHOWCASE === '1'

test('all 40 lessons open from the generated catalog and export their samples', async ({ page, request }) => {
  test.setTimeout(65000)
  const response = await request.get(isShowcase ? './snapshot.json' : '/api/scenarios')
  expect(response.ok()).toBe(true)
  const data = await response.json()
  const entries: { id: string; title: string }[] = isShowcase ? data.catalog.scenarios : data.scenarios
  expect(entries).toHaveLength(40)
  await page.goto('./#/techniques')
  await expect(page.locator('.technique-group')).toHaveCount(8)
  await expect(page.locator('.technique-card')).toHaveCount(40)
  for (const entry of entries) {
    await page.goto(`./#/lesson/${entry.id}`)
    await expect(page.getByRole('heading', { name: entry.title, exact: true, level: 1 })).toBeVisible()
  }
  await page.getByLabel('Sample fixture').selectOption('baseline')
  const downloaded = page.waitForEvent('download')
  await page.getByRole('button', { name: 'Download sample JSON' }).click()
  const file = await downloaded
  expect(file.suggestedFilename()).toBe('threathuntx-40-baseline.json')
  expect(JSON.parse(await readFile((await file.path())!, 'utf8'))).toMatchObject({ mode: 'baseline', synthetic_only: true, alerts: [] })
})

test('Detection Studio compares real fixture decisions and keeps a trial isolated', async ({ page, request }) => {
  await page.goto('./#/rules/02')
  const positive = page.getByRole('article').filter({ hasText: 'Positive fixture' })
  const noise = page.getByRole('article').filter({ hasText: 'Noisy control' })
  await expect(positive).toContainText('1 alert observed')
  await expect(positive.getByRole('listitem')).toHaveCount(3)
  await expect(noise).toContainText('0 alerts observed')
  if (isShowcase) {
    await expect(page.getByRole('button', { name: 'Compare fixtures' })).toHaveCount(0)
  } else {
    const original = await (await request.get('/api/scenarios/02/trial')).json()
    await page.getByLabel('Threshold', { exact: true }).fill('4')
    await page.getByRole('button', { name: 'Compare fixtures' }).click()
    await expect(positive).toContainText('0 alerts observed')
    await expect(page.getByText('The positive batch fell below the trial threshold.', { exact: false })).toBeVisible()
    await page.getByLabel('Threshold', { exact: true }).fill('1')
    await page.getByLabel('Group by').selectOption('host')
    await page.getByRole('button', { name: 'Compare fixtures' }).click()
    await expect(noise).toContainText('1 alert observed')
    await page.getByRole('button', { name: 'Reset trial' }).click()
    await expect(noise).toContainText('0 alerts observed')
    expect(await (await request.get('/api/scenarios/02/trial')).json()).toEqual(original)
  }
  const results = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze()
  expect(results.violations).toEqual([])
})

test('case pivots, saved notes, sanitized CSV, and printable evidence report', async ({ page }) => {
  const showcaseRequests: string[] = []
  page.on('request', request => {
    if (isShowcase && (request.method() !== 'GET' || new URL(request.url()).pathname.includes('/api/'))) showcaseRequests.push(request.url())
  })
  await page.goto('./#/lesson/02')
  await page.getByRole('button', { name: 'Replay & evidence' }).click()
  await page.getByRole('button', { name: isShowcase ? 'View positive sample' : 'Replay safe events' }).click()
  await page.getByRole('link', { name: 'Open evidence timeline' }).click()
  await expect(page.getByRole('heading', { name: 'Evidence timeline' })).toBeVisible()
  await page.getByRole('searchbox', { name: 'Search event fields' }).fill('02-positive-02')
  await expect(page.getByRole('list', { name: 'Evidence timeline in UTC' }).getByRole('listitem')).toHaveCount(1)
  await page.locator('.timeline summary').click()
  await page.getByRole('button', { name: 'Pivot by actor' }).click()
  await expect(page.getByLabel('Actor')).not.toHaveValue('')
  await page.getByRole('button', { name: 'Clear filters' }).click()
  await expect(page.getByLabel('Actor')).toHaveValue('')

  const note = '  =1+1\n<strong>literal evidence note</strong>'
  await page.getByLabel('Working hypothesis').fill('Review distinct MFA challenges.')
  await page.getByLabel('Triage decision').selectOption('investigate')
  await page.getByLabel('Analyst notes').fill(note)
  await page.getByLabel('Response decision').fill('Review the enrollment and identity timeline.')
  await page.getByRole('button', { name: 'Save case analysis' }).click()
  await expect(page.getByText('Case analysis saved in this browser.')).toBeVisible()
  await page.reload()
  await expect(page.getByLabel('Analyst notes')).toHaveValue(note)
  const jsonDownload = page.waitForEvent('download')
  await page.getByRole('button', { name: 'Case JSON' }).click()
  const json = JSON.parse(await readFile((await (await jsonDownload).path())!, 'utf8'))
  expect(json).toMatchObject({ schema_version: 1, synthetic_only: true, rule_id: 'THX-02', analysis: { disposition: 'investigate', notes: note } })
  expect(json.alerts[0].evidence).toContain('02-positive-02')
  const csvDownload = page.waitForEvent('download')
  await page.getByRole('button', { name: 'Case CSV' }).click()
  expect(await readFile((await (await csvDownload).path())!, 'utf8')).toContain(`"'${note}"`)
  await page.getByRole('link', { name: 'Printable report' }).click()
  await expect(page.getByRole('heading', { name: 'Case report' })).toBeVisible()
  await expect(page.getByText('<strong>literal evidence note</strong>', { exact: false })).toBeVisible()
  expect(await page.locator('.printable-case strong').count()).toBe(0)
  await page.emulateMedia({ media: 'print' })
  await expect(page.getByRole('button', { name: 'Print report' })).toBeHidden()
  const pdf = await page.pdf({ format: 'A4' })
  expect(pdf.toString('ascii', 0, 4)).toBe('%PDF')
  expect(showcaseRequests).toEqual([])
})
